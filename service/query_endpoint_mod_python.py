from mod_python import apache
import os.path
from app.handler.query_fma_handler import QueryStringFmaHandler

def handler(request):

    path = os.path.abspath(__file__)

    # are we the endpoint we want?
    if request.filename == path:

        headers = request.headers_in
        token = None
        if "token" in headers:
            token = headers["token"]

        query_fma_handler = QueryStringFmaHandler()
        request.content_type = query_fma_handler.getContentType()
        request.write(query_fma_handler.handle(request.args, token))

    return apache.OK
