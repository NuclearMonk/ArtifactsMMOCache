from schemas.request import Request, Response
from models.request import RequestModel, ResponseModel


def response_to_schema(response: ResponseModel) -> Response | None:
    if not response:
        return None
    return Response(id=response.id, code=response.code,headers=response.headers, body=response.body, timestamp=response.timestamp)


def request_to_schema(request: RequestModel) -> Request | None:
    if not request:
        return None
    return Request(id=request.id,
                   method=request.method,
                   url=request.url,
                   params=request.params,
                   headers= request.headers,
                   body=request.body,
                   response=response_to_schema(request.response),
                   timestamp=request.timestamp)
