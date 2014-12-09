from ..oal import OnlineApplicationLayer
import sys
import urlparse

class QueryStringFmaHandler(object):
    
    def handle(self, request_string, token):
        """
        handle a request_string (expects query string format) and a possible token (extracted from headers)
        """
        query_list = None

        try:
            query_list = urlparse.parse_qs(request_string)
        except:
            response = sys.exc_info()[0]

        if query_list is not None:
            try:
                oal = OnlineApplicationLayer()
                
                
                method_name = query_list['method'][0]
                del query_list['method']
                
                params_data = dict()
                for paramKey in query_list.iterkeys():
                    params_data[paramKey]=query_list[paramKey][0]
                    
                    
                methodPtr = getattr(oal, method_name)
                response_builder = methodPtr(params_data)

                response = ""
                for responseKey in response_builder.iterkeys():
                    response = response + str(response_builder[responseKey])

            except Exception as inst:
                response = "ERROR: " + str(type(inst)) + ": " + str(inst)
        else:
            response = "ERROR: Unable to parse request string"
        
        return response

    def getContentType(self):
        return  'text/plain'
