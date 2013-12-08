import unittest
from ..app.user.account import Account
from ..app.user.account import InvalidEmailAddressException
from ..app.user.account import PasswordIsIncorrectException
from ..app.user.account import TokenExpiredException

class TestAccount(unittest.TestCase):

    def test_create_valid_account(self):
        try:
        
            account = Account( email="abtest@gmail.com", password="password123456" )
            account.delete()
            assert account.isAccountCreated() == False
            account.create()
            assert account.isAccountCreated() == True
            assert account.getToken() is not None
            
            accountReload = Account(  email="abtest@gmail.com", password="password123456" )
            assert accountReload.isAccountCreated() == True
            assert accountReload.getToken() is not None
                        
            newToken = accountReload.getToken()
            
            accountReload = Account(  token=newToken )
            assert accountReload.getEmail() == "abtest@gmail.com"
            
            accountReload.delete()
            assert accountReload.isAccountCreated() == False
            assert accountReload.getToken() is None
            
        except InvalidEmailAddressException:
            self.fail("test_create_valid_account has valid email address but exception was raised!")
        except PasswordIsIncorrectException:
            self.fail("test_create_valid_account has no account but password exception raised!")
        except TokenExpiredException:
            self.fail("test_create_valid_account incorrectly raised invalid token!")
            
    def test_create_invalid_email_account(self):
        try:
            account = Account(  email="@$'D'@Zvzv@test.com", password="password123456" )
            self.fail("test_create_invalid_email_account had an invalid email but no exception was raised")
        except InvalidEmailAddressException:
            pass
        except PasswordIsIncorrectException:
            self.fail("test_create_invalid_email_account has no account but password exception raised!")
            
    def test_create_invalid_password_and_login_to_account(self):
        try:
            account = Account(  email="abtest@gmail.com", password="password123456" )
            account.delete()
            assert account.isAccountCreated() == False
            account.create()
            assert account.isAccountCreated() == True
            
            #wrong password
            accountReload = Account(  email="abtest@gmail.com", password="wrongpassword" )
            
            self.fail("test_create_invalid_email_account had an invalid password but no exception was raised")
            
        except InvalidEmailAddressException:
            self.fail("test_create_invalid_password_and_login_to_account had invalid password but invalid email address raised!")
        except PasswordIsIncorrectException:
            pass