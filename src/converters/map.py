

from models.map import MapModel
from schemas.map import MapContentSchema, MapSchema


def map_to_model(map: MapSchema) -> MapModel:
    m = MapModel()
    m.x = map.x
    m.y = map.y
    m.name = map.name
    m.skin = map.skin
    if map.content:
        m.content_type = map.content.type
        m.content_code = map.content.code
    return m


def map_to_schema(model: MapModel) -> MapSchema:
    return MapSchema(name=model.name,
                     skin=model.skin,
                     x=model.x,
                     y=model.y,
                     content=MapContentSchema(
                         type=model.content_type,
                         code=model.content_code) if model.content_type else None)
