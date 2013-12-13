from yahoo.income_statement import IncomeStatementManager
from user.account import Account
from user.account import EmailParameterNotSuppliedException
from user.account import PasswordParameterNotSuppliedException
from user.account import PasswordIsIncorrectException
from user.account import AccountEmailAlreadyExistsException
import logging
import base64

class OnlineApplicationLayer:

    def createAccount(self,params):
        """
        Create a new account to monitor a watchlist of securities
        
        B{Example JSON-RPC2 Request:}
        
        I{{"jsonrpc": "2.0", "method": "createAccount", "params": {"email":"alan@test.com", "password":"123456"}, "id": 1}}
        
        B{Example JSON-RPC2 Response:}
        
        I{{"jsonrpc": "2.0", "result": { "email": "alan@test.com" }, "id": 1}}
       
        @param params: keys:
        
        E{-} B{email} as I{string}
        
        E{-} B{password} as I{string}
        
        @type params: dictionary

        @return:  response keys:
        
        E{-} B{email} as I{string} the email that was request to be created. If a valid response (no error code) 
        """
        if "email" in params:
            if "password" in params:
                retObj = {"email":""}
                try:
                    account = Account( email=params["email"], password=params["password"] )
                except PasswordIsIncorrectException:
                    raise AccountEmailAlreadyExistsException( "Account with email " + params["email"]  + " already exists!" )
                account.create()
                retObj["email"] = params["email"]
                return retObj
            else:
                raise PasswordParameterNotSuppliedException("Request was missing required \"password\" parameter")
        else:
            raise EmailParameterNotSuppliedException("Request was missing required \"email\" parameter")
    
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