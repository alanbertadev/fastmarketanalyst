from yahoo.income_statement import IncomeStatementManager
from user.account import Account
from user.account import EmailParameterNotSuppliedException
from user.account import PasswordParameterNotSuppliedException
from user.account import PasswordIsIncorrectException
from user.account import AccountEmailAlreadyExistsException
from user.account import UserNotAuthenticatedException
import base64
from secure_oal import SecureOnlineApplicationLayer
from secure_oal import ParameterNotSuppliedException

class OnlineApplicationLayer(SecureOnlineApplicationLayer):
      
    def authenticate(self, params):
        """        
        Authenticate an account and receive a token

        B{Example JSON-RPC2 Request:}

        I{{"jsonrpc": "2.0", "method": "authenticate", "params": {"email":"alan@test.com", "password":"123456"}, "id": 1}}

        B{Example JSON-RPC2 Response:}

        I{{"jsonrpc": "2.0", "result": { "token": "57d1fc70-65f1-11e3-949a-0800200c9a66" }, "id": 1}}

        @param params: keys:

        E{-} B{email} as I{string}

        E{-} B{password} as I{string}

        @type params: dictionary

        @return:  response keys:

        E{-} B{token} as I{string} The token that must be supplied for future requests
        """
        if "email" in params:
            if "password" in params:
                ret_obj = {"token":""}
                account = Account(email=params["email"], password=params["password"])
                ret_obj["token"] = account.get_token()
                return ret_obj
            else:
                raise PasswordParameterNotSuppliedException("Request was missing required \"password\" parameter")
        else:
            raise EmailParameterNotSuppliedException("Request was missing required \"email\" parameter")

    def create_account(self, params):
        """
        Create a new account to monitor a watchlist of securities

        B{Example JSON-RPC2 Request:}

        I{{"jsonrpc": "2.0", "method": "create_account", "params": {"email":"alan@test.com", "password":"123456"}, "id": 1}}

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
                ret_obj = {"email":""}
                try:
                    account = Account(email=params["email"], password=params["password"])
                except PasswordIsIncorrectException:
                    raise AccountEmailAlreadyExistsException("Account with email " + params["email"] + " already exists!")
                account.create()
                ret_obj["email"] = params["email"]
                return ret_obj
            else:
                raise PasswordParameterNotSuppliedException("Request was missing required \"password\" parameter")
        else:
            raise EmailParameterNotSuppliedException("Request was missing required \"email\" parameter")

    def get_annual_income_statement_as_html(self, params):
        """
        Fetch(from Yahoo.com) the annual income statement of a given security

        B{Example JSON-RPC2 Request:}

        I{{"jsonrpc": "2.0", "method": "get_annual_income_statement_as_html", "params": {"symbol":"msft"}, "id": 1}}

        B{Example JSON-RPC2 Response:}

        I{{"jsonrpc": "2.0", "result": { "income_statement": "<base 64 encoded HTML>" }, "id": 1}}

        @param params: keys:

        E{-} B{symbol} as I{string}

        @type params: dictionary

        @return:  response keys:

        E{-} B{income_statement} as I{string} a Base64 encoded HTML of the annual income statement
        """
        # account = self._requires_token(params)
        ret_obj = {'income_statement':""}
        income_statement_manager = IncomeStatementManager(params['symbol'])
        ret_obj['income_statement'] = base64.b64encode(income_statement_manager.getAnnual().getHtml())
        return ret_obj

    def get_quarterly_income_statement_as_html(self, params):
        """
        Fetch(from Yahoo.com) the quarterly income statement of a given security

        B{Example JSON-RPC2 Request:}

        I{{"jsonrpc": "2.0", "method": "get_quarterly_income_statement_as_html", "params": {"symbol":"goog"}, "id": 1}}

        B{Example JSON-RPC2 Response:}

        I{{"jsonrpc": "2.0", "result": { "income_statement": "<base 64 encoded HTML>" }, "id": 1}}

        @param params: keys:

        E{-} B{symbol} as I{string}

        @type params: dictionary

        @return:  response keys:

        E{-} B{income_statement} as I{string} a Base64 encoded HTML of the quarterly income statement
        """
        # account = self._requires_token(params)
        ret_obj = {'income_statement':""}
        income_statement_manager = IncomeStatementManager(params['symbol'])
        ret_obj['income_statement'] = base64.b64encode(income_statement_manager.getQuarterly().getHtml())
        return ret_obj
    
    #
    # Begin _requires_token() service methods
    #
    
    def add_symbols_to_watch_list(self, params):
        """
        Add an array of symbols to the user's personal watch list of securities

        B{Example JSON-RPC2 Request:}

        I{{"jsonrpc": "2.0", "method": "add_symbols_to_watch_list", "params": { "watch_list": ["GOOG","MSFT"] }, "id": 1}}

        B{Example JSON-RPC2 Response:}

        I{{"jsonrpc": "2.0", "result": { "watch_list": ["GOOG","MSFT"] }, "id": 1}}

        @param params: keys:

        E{-} B{symbols} as I{array} of I{string}

        @type params: dictionary

        @return:  response keys:

        E{-} B{watch_list} as I{array} of I{string} each element is a security symbol that was added
        """
        account = self._requires_token(params)
        if "symbols" in params:
            symbols = params['symbols']
            if isinstance(symbols, list):
                for sym in symbols:
                    account.add_symbols_to_watch_list(sym)
                ret_obj = {'symbols':""}
                ret_obj['symbols'] = symbols
                return ret_obj
            else:
                raise ParameterNotSuppliedException("Request was missing required \"symbols\" parameter. The parameter must be an array of symbols.")
        else:
            raise ParameterNotSuppliedException("Request was missing required \"symbols\" parameter")
        
    def get_watch_list(self, params):
        """
        Get the currently authenticated user's personal watch list of securities

        B{Example JSON-RPC2 Request:}

        I{{"jsonrpc": "2.0", "method": "get_watch_list", "params": {}, "id": 1}}

        B{Example JSON-RPC2 Response:}

        I{{"jsonrpc": "2.0", "result": { "watch_list": ["GOOG","MSFT"] }, "id": 1}}

        @param params: keys:

        E{-} I{No params}

        @type params: dictionary

        @return:  response keys:

        E{-} B{watch_list} as I{array} of I{string} each element is a security symbol
        """
        account = self._requires_token(params)
        ret_obj = {"watch_list":[]}
        ret_obj['watch_list'] = account.get_watch_list()
        return ret_obj
