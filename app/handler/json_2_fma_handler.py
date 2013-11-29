import json
from ..oal import OnlineApplicationLayer

class Json2FmaHandler:
    
    def handle( self, requestString ):
    
        try:
            requestJsonObject = json.loads(requestString)
        except:
            requestJsonObject = None

        if requestJsonObject is not None:
            oal = OnlineApplicationLayer()
            methodName = requestJsonObject['method']
            paramsData = requestJsonObject['params']
            
            methodPtr = getattr(oal, methodName)
            responseBuilder = methodPtr(paramsData)
            responseId = requestJsonObject['id']
        
            response = {}
            response['id'] = responseId
            response['result'] = responseBuilder
            response['jsonrpc'] = "2.0"
            response = json.dumps(response)
        else:
            response = ""
            
        return response
        
        
    def getContentType(self):
        return  'application/json'