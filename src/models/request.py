from datetime import datetime, timezone
from typing import Any
from requests import get
from sqlalchemy import Column, DateTime
from sqlmodel import SQLModel, Field, Relationship, Session, create_engine
from ratelimiter import rate_session

class Request(SQLModel, table=True):
    __tablename__ = 'requests'
    id: int | None = Field(default=None, primary_key=True)
    method: str
    url: str
    body: str | None = None
    params: str | None = None
    response: 'Response' = Relationship(back_populates='request')
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=False), nullable=False))


class Response(SQLModel, table=True):
    __tablename__ = 'responses'
    id: int | None = Field(
        default=None, foreign_key='requests.id', primary_key=True)
    code: int
    body: str | None = None
    request: Request = Relationship(back_populates='response')
    timestamp: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))



sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)

def get_request(url: str, params: dict[str, Any] = None):
    with Session(engine) as session:
        req = Request(method='GET',url = url, params = str(params), timestamp=datetime.now(timezone.utc))
        resp = rate_session.get(url, params=params)
        if not resp.ok:
            return
        resp = Response(code = resp.status_code, body = resp.text,timestamp=datetime.now(timezone.utc))
        req.response = resp
        session.add(req)
        session.commit()


