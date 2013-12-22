import json
from ..oal import OnlineApplicationLayer
import sys

class Json2FmaHandler(object):
    
    def handle(self, request_string, token):
        """
        handle a request_string (expects JSON-RPC2 format) and a possible token (extracted from headers)
        """
        request_json_error = None

        try:
            request_json_object = json.loads(request_string)
        except:
            request_json_object = None
            request_json_error = sys.exc_info()[0]

        response_id = 0
        response = {}

        if request_json_object is not None:
            try:
                oal = OnlineApplicationLayer()
                method_name = request_json_object['method']
                params_data = request_json_object['params']
                
                if token is not None:
                    params_data['token'] = token
                
                methodPtr = getattr(oal, method_name)
                response_builder = methodPtr(params_data)
                response_id = request_json_object['id']
                response['result'] = response_builder
            except Exception as inst:
                response_builder = {}
                response_builder['code'] = -32099
                response_builder['message'] = str(type(inst)) + ": " + str(inst)
                response['error'] = response_builder
        else:
            response_builder = {}
            response_builder['code'] = -32700
            response_builder['message'] = 'Parse error'
            response['error'] = response_builder
        
        response['id'] = response_id
        response['jsonrpc'] = "2.0"
        response = json.dumps(response)
        
        return response
        
        
    def getContentType(self):
        return  'application/json'
