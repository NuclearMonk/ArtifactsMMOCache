

from enum import Enum
from pydantic import BaseModel

from schemas.paged import DataPageSchema

class CraftSkill(Enum):
    weaponcrafting = 'weaponcrafting'
    gearcrafting = 'gearcrafting'
    jewelrycrafting = 'jewelrycrafting'
    cooking = 'cooking'
    woodcutting = 'woodcutting'
    mining = 'mining'
    alchemy = 'alchemy'

class SimpleItemSchema(BaseModel):
    code: str
    quantity: int


class ItemEffectSchema(BaseModel):
    name: str
    value: int


class CraftSchema(BaseModel):
    skill: CraftSkill | None
    level: int | None
    items: list[SimpleItemSchema]
    quantity: int 


class ItemSchema(BaseModel):
    name: str
    code: str
    level: int
    type: str
    subtype: str
    description: str
    effects: list[ItemEffectSchema] | None = None
    craft: CraftSchema | None = None
    tradeable: bool


class ItemResponseSchema(BaseModel):
    data: ItemSchema

class DataPageItemSchema(DataPageSchema):
    data: list[ItemSchema] 

class DropRateSchema(BaseModel):
    code: str
    rate: int
    min_quantity: int
    max_quantity: int