from mod_python import apache
import json
import oal as OAL

def handler(request):
        request.content_type = 'application/json'
        response = ""
        
        try:
            requestString = request.read()
            
            #text_file = open("/var/tmp/ABERTA.txt", "w")

            #text_file.write(requestString)

            #text_file.close()
            
            #requestString = "{\"jsonrpc\": \"2.0\", \"method\": \"fetchIncomeStatement\", \"params\": {\"symbol\": \"GOOG\"}, \"id\": 0}"
            requestJsonObject = json.loads(requestString)
        except:
            requestJsonObject = None

        if requestJsonObject is not None:
            oal = OAL.OnlineApplicationLayer()
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
        
        request.write( response )
        return apache.OK