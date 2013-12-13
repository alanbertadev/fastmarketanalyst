from ..utils.redis_facade import RedisFacade
from ..utils.format_utils import FormatUtils
import json
import uuid

class InvalidEmailAddressException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
class PasswordIsIncorrectException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
class TokenExpiredException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
class PasswordParameterNotSuppliedException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
class EmailParameterNotSuppliedException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)
            
class AccountEmailAlreadyExistsException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

class Account:

    def __init__(self, **args):
        self.redis = RedisFacade()
        
        email = None
        if 'email' in args:
            email = args['email']
            
        password = None
        if 'password' in args:
            password = args['password']
            
        token = None
        if 'token' in args:
            token = args['token']
            
        self.accountExists = False
        
        self.email = None
        self.password = None
        self.watchSymbols = {}
        self.watchSymbols['symbols'] = []
        self.token = None
        
        if token is not None:
            if self.redis.exists( token ) == False:
                raise TokenExpiredException( token )
            else:
                email = self.redis.get( token )
                
        # Test if account has been constructed with a valid
        # email address
        if FormatUtils.isValidEmailAddressFormat( email ) == False:
            raise InvalidEmailAddressException( email )
            
        self.email = email
        self.emailKey = self.email + "_email"
        self.watchSymbolsKey = self.email + "_watchSymbols"
        self.passwordKey = self.email + "_password"
        
        if token is not None:
            if self.redis.exists( self.passwordKey ):
                password = self.redis.get( self.passwordKey )
        
        self.password = password
        
        if self.load() == True:
            if token is not None:
                self.setToken( token )
            else:
                self.setToken( str(uuid.uuid4()) )
            
    def isAccountCreated(self):
        return self.accountExists
        
    def create(self):
        if self.isAccountCreated():
            raise AccountEmailAlreadyExistsException(self.email)
        self.redis.set( self.emailKey, self.email )
        self.redis.set( self.passwordKey, self.password )
        self.redis.set( self.watchSymbolsKey, json.dumps(self.watchSymbols) )
        self.setToken( str(uuid.uuid4()) )
        self.accountExists = True
        
    def delete(self):
        if self.isAccountCreated():
            self.redis.delete( self.emailKey )
            self.redis.delete( self.passwordKey )
            self.redis.delete( self.watchSymbolsKey )
            self.accountExists = False

    def setToken(self, token):
        self.token = token
        self.redis.setex( self.token, self.email, 500 )
        
    def getToken(self):
        if self.accountExists:
            return self.token
        else:
            return None
        
    def getEmail(self):
        return self.email
        
    def getWatchList(self):
        return self.watchSymbols['symbols']
        
    def deleteSymbolInWatchlist(self, symbol):
        if symbol in self.watchSymbols['symbols']: self.watchSymbols['symbols'].remove(symbol)
        
    def addSymbolToWatchlist(self, symbol):
        self.watchSymbols['symbols'].append(symbol)
        
    def load(self):
        if self.redis.exists( self.emailKey ):
            if self.redis.get( self.passwordKey ) != self.password:
                raise PasswordIsIncorrectException( self.email )
            try:
                self.watchSymbolsKey = json.loads(  self.redis.get( self.watchSymbolsKey )  )['symbols']
            except:
                self.watchSymbols = {}
                self.watchSymbols['symbols'] = []
            self.accountExists = True
            self.setToken(str(uuid.uuid4())) 