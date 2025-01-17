

from enum import Enum
from pydantic import BaseModel

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

class DataPageItemSchema(BaseModel):
    data: list[ItemSchema] 
    total:  int | None
    page: int | None
    size: int | None
    pages : int | None