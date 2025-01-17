
from pydantic import BaseModel

from schemas.item import DropRateSchema
from schemas.paged import DataPageSchema




class MonsterSchema(BaseModel):
    name: str 
    code: str
    level: int
    hp: int 
    attack_fire: int
    attack_earth: int 
    attack_water: int
    attack_air: int
    res_fire: int 
    res_earth: int
    res_water: int 
    res_air: int
    min_gold: int
    max_gold: int
    drops: list[DropRateSchema]

class MonsterResponseSchema(BaseModel):
    data: MonsterSchema

class DataPageMonsterSchema(DataPageSchema):
    data: list[MonsterSchema]