from datetime import datetime
from tokenize import String
from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class RequestModel(Base):
    __tablename__ = 'requests'
    id: Mapped[int | None] = mapped_column(primary_key=True)
    method: Mapped[str]
    url: Mapped[str]
    params: Mapped[str | None]
    headers: Mapped[str]
    body: Mapped[str | None]
    response: Mapped['ResponseModel'] = relationship(back_populates='request')
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=False))

    def __init__(self, method: str, url: str,  headers: str, timestamp: datetime, params: str | None = None, body: str | None = None):
        super().__init__()
        self.method = method
        self.url = url
        self.params = params
        self.headers = headers
        self.body = body
        self.timestamp = timestamp


class ResponseModel(Base):
    __tablename__ = 'responses'
    id: Mapped[int] = mapped_column(
        ForeignKey('requests.id'), primary_key=True)
    code: Mapped[int]
    headers: Mapped[str]
    body: Mapped[str | None]
    request: Mapped[RequestModel] = relationship(back_populates='response')
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    def __init__(self, code: int, headers: str, body: str, timestamp: datetime):
        super().__init__()
        self.code = code
        self.headers = headers
        self.body = body
        self.timestamp = timestamp
