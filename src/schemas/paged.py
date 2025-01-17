

from pydantic import BaseModel


class DataPageSchema(BaseModel):
    total:  int | None
    page: int | None
    size: int | None
    pages : int | None