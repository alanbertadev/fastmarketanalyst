import unittest
from ..app.yahoo.income_statement import IncomeStatement

class TestIncomeStatement(unittest.TestCase):

    def test_extract_income_statement_from_string_with_null_input(self):
        iStmt = IncomeStatement()
        assert iStmt.extractIncomeStatementFromString(None) == None

