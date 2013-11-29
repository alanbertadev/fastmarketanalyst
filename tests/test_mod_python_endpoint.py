import unittest
from ..app.handler.json_2_fma_handler import Json2FmaHandler

class TestJson2FmaHandler(unittest.TestCase):

    def test_fetch_google_annual_income_statement_as_html(self):
    
        json2FmaHandler = Json2FmaHandler()
        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"getAnnualIncomeStatementAsHtml\", \"params\": {\"symbol\": \"GOOG\"}, \"id\": 0}"
    
        assert json2FmaHandler.handle( testString ) is not None
        
    def test_fetch_google_quarterly_income_statement_as_html(self):
    
        json2FmaHandler = Json2FmaHandler()
        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"getQuarterlyIncomeStatementAsHtml\", \"params\": {\"symbol\": \"GOOG\"}, \"id\": 0}"
    
        assert json2FmaHandler.handle( testString ) is not None
