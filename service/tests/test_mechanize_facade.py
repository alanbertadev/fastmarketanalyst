import unittest
import mechanize
import cookielib
from ..app.utils.mechanize_facade import MechanizeFacade

class TestMechanizeFacade(unittest.TestCase):

    def test_fetch_simple_test_html_file_contents(self):
        browser = MechanizeFacade()
        assert browser.fetchSimpleURLAsString("http://jenkins.alanbertadev.com/test.html") == "test"

