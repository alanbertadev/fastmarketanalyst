import json
import unittest
from ..app.utils.redis_facade import RedisFacade
from ..app.handler.json_2_fma_handler import Json2FmaHandler

class TestJson2FmaHandler(unittest.TestCase):

    def test_create_new_account(self):

        redis = RedisFacade()

        json2FmaHandler = Json2FmaHandler()
        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"create_account\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"

        resData = json2FmaHandler.handle( testString, None )

        redis.delete( "alanbertatesting@test.com_email" )
        redis.delete( "alanbertatesting@test.com_password" )
        redis.delete( "alanbertatesting@test.com_watchSymbols" )

        assert json.loads(resData)['result'] is not None

    def test_authenticate(self):

        redis = RedisFacade()

        json2FmaHandler = Json2FmaHandler()
        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"create_account\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"

        resData = json2FmaHandler.handle( testString, None )

        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"authenticate\", \"params\": {\"email\": \"alanbertatesting@test.com\", \"password\":\"123456\"}, \"id\": 0}"

        resData = json2FmaHandler.handle( testString, None )

        resultData = json.loads(resData)['result']

        assert resultData['token'] is not None

        redis.delete( "alanbertatesting@test.com_email" )
        redis.delete( "alanbertatesting@test.com_password" )
        redis.delete( "alanbertatesting@test.com_watchSymbols" )

    def test_fetch_google_annual_income_statement_as_html(self):

        json2FmaHandler = Json2FmaHandler()
        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"get_annual_income_statement_as_html\", \"params\": {\"symbol\": \"GOOG\"}, \"id\": 0}"

        assert json.loads(json2FmaHandler.handle( testString, None ))['result'] is not None

    def test_fetch_google_quarterly_income_statement_as_html(self):

        json2FmaHandler = Json2FmaHandler()
        testString =  "{\"jsonrpc\": \"2.0\", \"method\": \"get_quarterly_income_statement_as_html\", \"params\": {\"symbol\": \"GOOG\"}, \"id\": 0}"

        assert json.loads(json2FmaHandler.handle( testString, None ))['result'] is not None

    def test_empty_request(self):

        json2FmaHandler = Json2FmaHandler()
        testString = ""
        resultObj = json.loads(json2FmaHandler.handle( testString, None ))

        assert 'result' not in resultObj 
        assert 'error' in resultObj
        assert resultObj['error']['code'] == -32700