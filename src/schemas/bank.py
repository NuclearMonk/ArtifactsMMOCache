
from pydantic import BaseModel

from schemas.item import SimpleItemSchema
from schemas.paged import DataPageSchema


class BankSchema(BaseModel):
    slots: int 
    expansions: int
    next_expansion_cost: int
    gold: int


class BankResponseSchema(BaseModel):
    data: BankSchema

class DataPageBankItemSchema(DataPageSchema):
    data : list[SimpleItemSchema]