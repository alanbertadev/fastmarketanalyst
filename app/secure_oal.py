from user.account import Account
from user.account import UserNotAuthenticatedException

class ParameterNotSuppliedException(Exception):
        def __init__(self, value):
            self.value = value
        def __str__(self):
            return repr(self.value)

class SecureOnlineApplicationLayer(object):
    
    def _requires_token(self, params):
        if "token" in params:
            tokenParam = params['token']
            return Account(token=tokenParam)
        else:
            raise UserNotAuthenticatedException("Authentication token has expired!")
                
    
