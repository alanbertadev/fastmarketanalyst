import unittest
from ..app.yahoo.income_statement import IncomeStatementManager

class TestIncomeStatement(unittest.TestCase):

    def test_extract_income_statement_from_string_with_null_input(self):
        iStmt = IncomeStatementManager(None)
        assert iStmt.extractIncomeStatementFromString(None) == None

    def test_fetch_annual_income_statement_MSFT(self):
        MSFT_iStmt = IncomeStatementManager("MSFT")
        response = MSFT_iStmt.getAnnual().getHtml()
        assert response is not None
        
    def test_fetch_quarterly_income_statement_MSFT(self):
        MSFT_iStmt = IncomeStatementManager("MSFT")
        response = MSFT_iStmt.getQuarterly().getHtml()
        assert response is not None