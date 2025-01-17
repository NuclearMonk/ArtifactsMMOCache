
from pydantic import BaseModel

from schemas.item import SimpleItemSchema


class BankSchema(BaseModel):
    slots: int 
    expansions: int
    next_expansion_cost: int
    gold: int


class BankResponseSchema(BaseModel):
    data: BankSchema

class BankItemResponseSchema(BaseModel):
    items : list[SimpleItemSchema]