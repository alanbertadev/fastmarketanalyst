import unittest
from ..app.yahoo.income_statement import IncomeStatement

class TestIncomeStatement(unittest.TestCase):

    def test_extract_income_statement_from_string_with_null_input(self):
        iStmt = IncomeStatement()
        assert iStmt.extractIncomeStatementFromString(None) == None

    def test_fetch_annual_income_statement_MSFT(self):
        iStmt = IncomeStatement()
        response = iStmt.fetchAnnualFromYahooAsHtml( "MSFT" )
        assert response is not None
        
    def test_fetch_quarterly_income_statement_MSFT(self):
        iStmt = IncomeStatement()
        response = iStmt.fetchQuarterlyFromYahooAsHtml( "MSFT" )
        assert response is not None