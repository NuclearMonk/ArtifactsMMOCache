

from pydantic import BaseModel

from schemas.paged import DataPageSchema


class MapContentSchema(BaseModel):
    type: str
    code: str


class MapSchema(BaseModel):
    name: str
    skin: str
    x: int
    y: int
    content: MapContentSchema | None


class MapResponseSchema(BaseModel):
    data: MapSchema

class DataPageMapSchema(DataPageSchema):
    data : list[MapSchema]