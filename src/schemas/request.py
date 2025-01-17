from datetime import datetime
from pydantic import BaseModel


class Request(BaseModel):
    id: int | None
    method: str
    url: str
    headers: str
    body: str | None
    params: str | None
    response: 'Response'
    timestamp: datetime


class Response(BaseModel):
    id: int
    code: int
    headers: str
    body: str | None
    timestamp: datetime