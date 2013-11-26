import unittest
import mechanize
import cookielib
from ..app.utils.mechanize_facade import MechanizeFacade

class TestMechanizeFacade(unittest.TestCase):

    def test_fetch_simple_test_html_file_contents(self):
        browser = MechanizeFacade()
        assert browser.fetchSimpleURLAsString("http://jenkins.alanbertadev.com/test.html") == "test"
        
    def test_fetch_yahoo_google_annual_income_statement(self):
        browser = MechanizeFacade()
        assert browser.fetchSimpleURLAsString("http://finance.yahoo.com/q/is?s=GOOG+Income+Statement&annual") is not None

