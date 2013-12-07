from yahoo.income_statement import IncomeStatementManager
import logging
import base64

class OnlineApplicationLayer:
    
    def getAnnualIncomeStatementAsHtml(self, params):
        """
        Fetch(from Yahoo.com) the annual income statement of a given security
        
        B{Example JSON-RPC2 Request:}
        
        I{{"jsonrpc": "2.0", "method": "getAnnualIncomeStatementAsHtml", "params": {"symbol":"msft"}, "id": 1}}
        
        B{Example JSON-RPC2 Response:}
        
        I{{"jsonrpc": "2.0", "result": { "IncomeStatement": "<base 64 encoded HTML>" }, "id": 1}}
       
        @param params: keys:
        
        E{-} B{symbol} as I{string}
        
        @type params: dictionary

        @return:  response keys:
        
        E{-} B{IncomeStatement} as I{string} a Base64 encoded HTML of the annual income statement
        """
        retObj = {'IncomeStatement':""}
        incomeStatementMgr = IncomeStatementManager(params['symbol'])
        retObj['IncomeStatement'] = base64.b64encode(incomeStatementMgr.getAnnual().getHtml())
        return retObj

    def getQuarterlyIncomeStatementAsHtml(self, params):
        """
        Fetch(from Yahoo.com) the quarterly income statement of a given security
        
        B{Example JSON-RPC2 Request:}
        
        I{{"jsonrpc": "2.0", "method": "getQuarterlyIncomeStatementAsHtml", "params": {"symbol":"goog"}, "id": 1}}

        B{Example JSON-RPC2 Response:}
        
        I{{"jsonrpc": "2.0", "result": { "IncomeStatement": "<base 64 encoded HTML>" }, "id": 1}}
        
        @param params: keys:
        
        E{-} B{symbol} as I{string}
        
        @type params: dictionary

        @return:  response keys:
        
        E{-} B{IncomeStatement} as I{string} a Base64 encoded HTML of the quarterly income statement
        """
        retObj = {'IncomeStatement':""}
        incomeStatementMgr = IncomeStatementManager(params['symbol'])
        retObj['IncomeStatement'] = base64.b64encode(incomeStatementMgr.getQuarterly().getHtml())
        return retObj