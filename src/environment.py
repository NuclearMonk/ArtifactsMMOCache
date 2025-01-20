

from datetime import datetime, timezone
from os import path
from pathlib import Path
from typing import Any

from pyrate_limiter import Duration, Limiter, RequestRate, SQLiteBucket
from requests_ratelimiter import LimiterSession
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from models.base import Base
from models.request import RequestModel, ResponseModel
from models.bank import BankModel, BankItemModel
from models.item import ItemModel, ItemEffectModel, CraftItemModel
from models.monster import MonsterDropRateModel, MonsterModel
from models.resource import ResourceDropRateModel, ResourceModel
from models.map import MapModel
from requests import Response

__CREDENTIALS_PATH = Path('data/apikey')
__SQLITE_PATH = "data/database.db"
__SQLITE_URL = f"sqlite:///{__SQLITE_PATH}"


def get_api_key():
    if path.exists(__CREDENTIALS_PATH):
        with open(__CREDENTIALS_PATH) as f:
            return f.read().strip()
    else:
        print('API KEY FILE  NOT FOUND')
        return None


BASE_URL = 'https://api.artifactsmmo.com'
ENGINE = create_engine(__SQLITE_URL)
HEADERS = {'Accept': 'application/json',
           'Authorization': f'Bearer {get_api_key()}'}


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


__PER_SECOND = RequestRate(16, Duration.SECOND)
__PER_MINUTE = RequestRate(200, Duration.MINUTE)
__PER_HOUR = RequestRate(7200, Duration.HOUR)
__LIMITER = Limiter(__PER_SECOND, __PER_MINUTE, __PER_HOUR)
__RATE_SESSION = LimiterSession(limiter=__LIMITER, bucket_class=SQLiteBucket)


def get(url: str, params: dict[str, Any] = None) -> Response:
    with Session(ENGINE) as session:
        req = RequestModel(method='GET', url=url, params=str(
            params), headers=str(HEADERS), timestamp=datetime.now(timezone.utc))
        resp = __RATE_SESSION.get(url, params=params, headers=HEADERS)
        r = ResponseModel(code=resp.status_code, headers=str(resp.headers), body=resp.text,
                          timestamp=datetime.now(timezone.utc))
        req.response = r
        session.add(req)
        session.commit()
        return resp


if __name__ == '__main__':
    Base.metadata.create_all(ENGINE)
