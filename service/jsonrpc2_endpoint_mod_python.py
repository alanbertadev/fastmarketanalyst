from mod_python import apache
from app.handler.json_2_fma_handler import Json2FmaHandler

def handler(request):

    headers = request.headers_in
    token = None
    if "token" in headers:
        token = headers["token"]

    json2_fma_handler = Json2FmaHandler()
    request.content_type = json2_fma_handler.getContentType()
    request.write(json2_fma_handler.handle( request.read(), token ) )

    return apache.OK