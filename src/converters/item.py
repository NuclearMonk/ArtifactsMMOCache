

from models.item import CraftItemModel, CraftModel, ItemEffectModel, ItemModel
from schemas.item import CraftSchema, ItemEffectSchema, ItemSchema, SimpleItemSchema


def craft_to_model(craft: CraftSchema) -> CraftModel:
    m = CraftModel()
    m.skill = craft.skill
    m.level = craft.level
    m.items = [CraftItemModel(item.code, item.quantity)
               for item in craft.items]
    m.quantity = craft.quantity
    return m


def craft_to_schema(model: CraftModel) -> CraftSchema:
    return CraftSchema(skill=model.skill,
                       level=model.level,
                       items=[SimpleItemSchema(
                           code=item.item_code,
                           quantity=item.quantity) for item in model.items],
                       quantity=model.quantity)


def effect_to_model(effect: ItemEffectSchema) -> ItemEffectModel:
    m = ItemEffectModel()
    m.effect_name = effect.name
    m.value = effect.value
    return m


def effect_to_schema(model: ItemEffectModel) -> ItemEffectSchema:
    return ItemEffectSchema(name=model.effect_name, value=model.value)


def item_to_model(item: ItemSchema) -> ItemModel:
    m = ItemModel()
    m.code = item.code
    m.name = item.name
    m.level = item.level
    m.type = item.type
    m.subtype = item.subtype
    m.description = item.description
    m.tradeable = item.tradeable
    if item.craft:
        m.craft = craft_to_model(item.craft)
    else:
        item.craft = None
    if item.effects:
        m.effects = [effect_to_model(effect) for effect in item.effects]
    return m


def item_to_schema(model: ItemModel) -> ItemSchema:
    return ItemSchema(
        name=model.name,
        code=model.code,
        level=model.level,
        type=model.type,
        subtype=model.subtype,
        description=model.description,
        effects=[effect_to_schema(
            effect) for effect in model.effects] if model.effects else None,
        craft=craft_to_schema(model.craft) if model.craft else None,
        tradeable=model.tradeable
    )
