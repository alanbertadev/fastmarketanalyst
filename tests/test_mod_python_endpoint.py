import json
import unittest
from ..app.utils.redis_facade import RedisFacade
from ..app.handler.json_2_fma_handler import Json2FmaHandler
import sys

class TestJson2FmaHandler(unittest.TestCase):
    
    def test_create_new_account_and_get_empty_watchlist(self):

        redis = RedisFacade()
        
        try:
        
            # create new account
    
            json2FmaHandler = Json2FmaHandler()
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"create_account\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, None)
            assert json.loads(resData)['result'] is not None
            
            # authenticate and get token
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"authenticate\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, None)
            resultData = json.loads(resData)['result']
            assert resultData['token'] is not None
            
            # get empty watch list
            
            token = resultData['token']
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"get_watch_list\", \"params\": {}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, token)
            resultData = json.loads(resData)['result']
            assert resultData['watch_list'] is not None
            
        except:
            print sys.exc_info()
            redis.delete("alanbertatesting@test.com_email")
            redis.delete("alanbertatesting@test.com_password")
            redis.delete("alanbertatesting@test.com_watchSymbols")
            self.fail("Exception occurred during execution")

        # reset account

        redis.delete("alanbertatesting@test.com_email")
        redis.delete("alanbertatesting@test.com_password")
        redis.delete("alanbertatesting@test.com_watchSymbols")
        
    def test_create_new_account_and_add_to_watchlist(self):

        redis = RedisFacade()
        
        try:
        
            # create new account
    
            json2FmaHandler = Json2FmaHandler()
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"create_account\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, None)
            assert json.loads(resData)['result'] is not None
            
            # authenticate and get token
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"authenticate\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, None)
            resultData = json.loads(resData)['result']
            assert resultData['token'] is not None
            token = resultData['token']
            
            # add GOOG, MSFT, and AMZN to watchlist
            print "Adding GOOG, MSFT, and AMZN to watchlist"
            
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"add_symbols_to_watch_list\", \"params\": {\"symbols\": [\"GOOG\",\"MSFT\",\"AMZN\"]}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, token)
            resultData = json.loads(resData)['result']
            assert resultData['symbols'] is not None
            
            # get 3 symbol (GOOG,MSFT,AMZN) watch list
            print "Getting 3 symbol (GOOG,MSFT,AMZN) watch list"
            
            testString = "{\"jsonrpc\": \"2.0\", \"method\": \"get_watch_list\", \"params\": {}, \"id\": 0}"
            resData = json2FmaHandler.handle(testString, token)
            resultData = json.loads(resData)['result']
            assert resultData['watch_list'] is not None
            
            print "Setting local watch_list_test"
            watch_list_test = resultData['watch_list']
            
            print "Local watch list is " + str(len(watch_list_test))
            assert len(watch_list_test) == 3
            
            for sym in watch_list_test:
                if sym != "GOOG" and sym != "MSFT" and sym != "AMZN":
                    self.fail("Symbols were not stored correctly!")
            
        except:
            print sys.exc_info()
            redis.delete("alanbertatesting@test.com_email")
            redis.delete("alanbertatesting@test.com_password")
            redis.delete("alanbertatesting@test.com_watchSymbols")
            self.fail("Exception occurred during execution")

        # reset account

        redis.delete("alanbertatesting@test.com_email")
        redis.delete("alanbertatesting@test.com_password")
        redis.delete("alanbertatesting@test.com_watchSymbols")

    def test_create_new_account(self):

        redis = RedisFacade()

        json2FmaHandler = Json2FmaHandler()
        testString = "{\"jsonrpc\": \"2.0\", \"method\": \"create_account\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"

        resData = json2FmaHandler.handle(testString, None)

        redis.delete("alanbertatesting@test.com_email")
        redis.delete("alanbertatesting@test.com_password")
        redis.delete("alanbertatesting@test.com_watchSymbols")

        assert json.loads(resData)['result'] is not None

    def test_authenticate(self):

        redis = RedisFacade()

        json2FmaHandler = Json2FmaHandler()
        testString = "{\"jsonrpc\": \"2.0\", \"method\": \"create_account\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"

        resData = json2FmaHandler.handle(testString, None)

        testString = "{\"jsonrpc\": \"2.0\", \"method\": \"authenticate\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"

        resData = json2FmaHandler.handle(testString, None)

        resultData = json.loads(resData)['result']

        assert resultData['token'] is not None

        redis.delete("alanbertatesting@test.com_email")
        redis.delete("alanbertatesting@test.com_password")
        redis.delete("alanbertatesting@test.com_watchSymbols")

    def test_fetch_google_annual_income_statement_as_html(self):

        json2FmaHandler = Json2FmaHandler()
        testString = "{\"jsonrpc\": \"2.0\", \"method\": \"get_annual_income_statement_as_html\", \"params\": {\"symbol\": \"GOOGL\"}, \"id\": 0}"

        assert json.loads(json2FmaHandler.handle(testString, None))['result'] is not None

    def test_fetch_google_quarterly_income_statement_as_html(self):

        json2FmaHandler = Json2FmaHandler()
        testString = "{\"jsonrpc\": \"2.0\", \"method\": \"get_quarterly_income_statement_as_html\", \"params\": {\"symbol\": \"GOOGL\"}, \"id\": 0}"

        assert json.loads(json2FmaHandler.handle(testString, None))['result'] is not None

    def test_empty_request(self):

        json2FmaHandler = Json2FmaHandler()
        testString = ""
        resultObj = json.loads(json2FmaHandler.handle(testString, None))

        assert 'result' not in resultObj 
        assert 'error' in resultObj
        assert resultObj['error']['code'] == -32700
