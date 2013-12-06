import unittest
from ..app.utils.format_utils import FormatUtils

class TestFormatUtils(unittest.TestCase):

    def test_invalid_symbols_email_address(self):
        assert FormatUtils.isValidEmailAddressFormat( "@$'D'@Zvzv@test.com" ) == False
        
    def test_invalid_domain_email_address(self):
        assert FormatUtils.isValidEmailAddressFormat( "test@no" ) == False
        
    def test_valid_normal_email_address(self):
        assert FormatUtils.isValidEmailAddressFormat( "test@alan.com" ) == True
        
    def test_valid_period_in_email_address(self):
        assert FormatUtils.isValidEmailAddressFormat( "test.2@alan.com" ) == True
        
    def test_valid_plus_in_email_address(self):
        assert FormatUtils.isValidEmailAddressFormat( "test+test2@alan.com" ) == True