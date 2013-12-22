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
            
class UserNotAuthenticatedException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

class Account(object):

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
        self.watch_symbols = {}
        self.watch_symbols['symbols'] = []
        self.token = None
        
        if token is not None:
            if self.redis.exists(token) == False:
                raise TokenExpiredException(token)
            else:
                email = self.redis.get(token)
                
        # Test if account has been constructed with a valid
        # email address
        if FormatUtils.isValidEmailAddressFormat(email) == False:
            raise InvalidEmailAddressException(email)
            
        self.email = email
        self.email_key = self.email + "_email"
        self.watch_symbolsKey = self.email + "_watch_symbols"
        self.password_key = self.email + "_password"
        
        if token is not None:
            if self.redis.exists(self.password_key):
                password = self.redis.get(self.password_key)
        
        self.password = password
        
        if self.load() == True:
            if token is not None:
                self.set_token(token)
            else:
                self.set_token(str(uuid.uuid4()))
            
    def is_account_created(self):
        return self.accountExists
        
    def create(self):
        if self.is_account_created():
            raise AccountEmailAlreadyExistsException(self.email)
        self.redis.set(self.email_key, self.email)
        self.redis.set(self.password_key, self.password)
        self.redis.set(self.watch_symbolsKey, json.dumps(self.watch_symbols))
        self.set_token(str(uuid.uuid4()))
        self.accountExists = True
        
    def delete(self):
        if self.is_account_created():
            self.redis.delete(self.email_key)
            self.redis.delete(self.password_key)
            self.redis.delete(self.watch_symbolsKey)
            self.accountExists = False

    def set_token(self, token):
        self.token = token
        self.redis.setex(self.token, self.email, 500)
        
    def get_token(self):
        if self.accountExists:
            return self.token
        else:
            return None
        
    def get_email(self):
        return self.email
        
    def get_watch_list(self):
        return self.watch_symbols['symbols']
        
    def delete_symbol_in_watchlist(self, symbol):
        if symbol in self.watch_symbols['symbols']: 
            self.watch_symbols['symbols'].remove(symbol)
            self.redis.set(self.watch_symbolsKey, json.dumps(self.watch_symbols))
        
    def add_symbol_to_watchlist(self, symbol):
        self.watch_symbols['symbols'].append(symbol)
        self.redis.set(self.watch_symbolsKey, json.dumps(self.watch_symbols))
        
    def load(self):
        if self.redis.exists(self.email_key):
            if self.redis.get(self.password_key) != self.password:
                raise PasswordIsIncorrectException(self.email)
            try:
                self.watch_symbolsKey = json.loads(self.redis.get(self.watch_symbolsKey))['symbols']
            except:
                self.watch_symbols = {}
                self.watch_symbols['symbols'] = []
            self.accountExists = True
            self.set_token(str(uuid.uuid4())) 
