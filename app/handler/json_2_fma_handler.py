import json
from ..oal import OnlineApplicationLayer
import sys

class Json2FmaHandler:
    
    def handle( self, requestString ):
    
        requestJsonError = None
    
        try:
            requestJsonObject = json.loads(requestString)
        except:
            requestJsonObject = None
            requestJsonError = sys.exc_info()[0]
            
        responseId = 0
        response = {}

        if requestJsonObject is not None:
            oal = OnlineApplicationLayer()
            methodName = requestJsonObject['method']
            paramsData = requestJsonObject['params']
            
            methodPtr = getattr(oal, methodName)
            responseBuilder = methodPtr(paramsData)
            responseId = requestJsonObject['id']
            response['result'] = responseBuilder
        else:
            responseBuilder = {}
            responseBuilder['code'] = -32700
            responseBuilder['message'] = 'Parse error'
            response['error'] = responseBuilder
        
        response['id'] = responseId
        response['jsonrpc'] = "2.0"
        response = json.dumps(response)
        
        return response
        
        
    def getContentType(self):
        return  'application/json'