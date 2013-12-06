from ..utils.redis_facade import RedisFacade
from ..utils.format_utils import FormatUtils
import json

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

class Account:

    def __init__(self, email, password):
        self.redis = RedisFacade()
        
        self.accountExists = False
        
        self.email = None
        self.password = None
        self.watchSymbols = {}
        self.watchSymbols['symbols'] = []
        
        # Test if account has been constructed with a valid
        # email address
        if FormatUtils.isValidEmailAddressFormat( email ) == False:
            raise InvalidEmailAddressException( email )
            
        self.email = email
        self.password = password
        
        self.emailKey = self.email + "_email"
        self.watchSymbolsKey = self.email + "_watchSymbols"
        self.passwordKey = self.email + "_password"
        
        if self.load() == True:
            self.accountExists = True
            
    def isAccountCreated(self):
        return self.accountExists
        
    def create(self):
        print json.dumps(self.watchSymbols)
        self.redis.set( self.emailKey, self.email )
        self.redis.set( self.passwordKey, self.password )
        self.redis.set( self.watchSymbolsKey, json.dumps(self.watchSymbols) )
        self.accountExists = True
        
    def delete(self):
        self.redis.delete( self.emailKey )
        self.redis.delete( self.passwordKey )
        self.redis.delete( self.watchSymbolsKey )
        self.accountExists = False
        
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