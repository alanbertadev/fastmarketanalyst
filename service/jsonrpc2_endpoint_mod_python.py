from mod_python import apache
from ..app.handler.json_2_fma_handler import Json2FmaHandler

def handler(request):

    json2FmaHandler = Json2FmaHandler()
    request.content_type = json2FmaHandler.getContentType()
    request.write(json2FmaHandler.handle( request.read()))

    return apache.OK