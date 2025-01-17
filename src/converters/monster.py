

from models.monster import DropRateModel, MonsterModel
from schemas.item import DropRateSchema
from schemas.monster import MonsterSchema


def drop_rate_to_model(drop_rate: DropRateSchema) -> DropRateModel:
    m = DropRateModel()
    m.item_code = drop_rate.code
    m.rate = drop_rate.rate
    m.min_quantity = drop_rate.min_quantity
    m.max_quantity = drop_rate.max_quantity
    return m


def drop_rate_to_schema(model: DropRateModel) -> DropRateSchema:
    return DropRateSchema(code=model.item_code,
                          rate=model.rate,
                          min_quantity=model.min_quantity,
                          max_quantity=model.max_quantity)


def monster_to_model(monster: MonsterSchema) -> MonsterModel:
    m = MonsterModel()
    m.code = monster.code
    m.name = monster.name
    m.level = monster.level
    m.hp = monster.hp
    m.attack_fire = monster.attack_fire
    m.attack_earth = monster.attack_earth
    m.attack_water = monster.attack_water
    m.attack_air = monster.attack_air
    m.res_fire = monster.res_fire
    m.res_earth = monster.res_earth
    m.res_water = monster.res_water
    m.res_air = monster.res_air
    m.min_gold = monster.min_gold
    m.max_gold = monster.max_gold
    m.drops = [drop_rate_to_model(drop) for drop in monster.drops]
    return m


def monster_to_schema(model: MonsterModel) -> MonsterSchema:
    return MonsterSchema(name=model.name,
                         code=model.code,
                         level=model.level,
                         hp=model.hp,
                         attack_fire=model.attack_fire,
                         attack_earth=model.attack_earth,
                         attack_water=model.attack_water,
                         attack_air=model.attack_air,
                         res_fire=model.res_fire,
                         res_earth=model.res_earth,
                         res_water=model.res_water,
                         res_air=model.res_air,
                         min_gold=model.min_gold,
                         max_gold=model.max_gold,
                         drops=[drop_rate_to_schema(drop)
                                for drop in model.drops]
                         )
