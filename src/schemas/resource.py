



from enum import Enum
from pydantic import BaseModel

from schemas.item import DropRateSchema
from schemas.paged import DataPageSchema


class GatheringSkill(Enum):
    mining = 'mining'
    woodcutting = 'woodcutting'
    fishing = 'fishing'
    alchemy = 'alchemy'


class ResourceSchema(BaseModel):
    name: str 
    code: str
    skill: GatheringSkill
    level: int 
    drops: list[DropRateSchema]


class ResourceResponseSchema(BaseModel):
    data: ResourceSchema

class DataPageResourceSchema(DataPageSchema):
    data: list[ResourceSchema]