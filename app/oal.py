from yahoo.income_statement import IncomeStatementManager
import logging
import base64

class OnlineApplicationLayer:
            
        def getAnnualIncomeStatementAsHtml(self, params):
            retObj = {'IncomeStatement':""}
            incomeStatementMgr = IncomeStatementManager(params['symbol'])
            retObj['IncomeStatement'] = base64.b64encode(incomeStatementMgr.getAnnual().getHtml())
            return retObj
            
        def getQuarterlyIncomeStatementAsHtml(self, params):
            retObj = {'IncomeStatement':""}
            incomeStatementMgr = IncomeStatementManager(params['symbol'])
            retObj['IncomeStatement'] = base64.b64encode(incomeStatementMgr.getQuarterly().getHtml())
            return retObj