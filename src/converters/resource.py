

from models.resource import ResourceDropRateModel, ResourceModel
from schemas.item import DropRateSchema
from schemas.resource import ResourceSchema


def resource_drop_to_model(drop_rate: DropRateSchema) -> ResourceDropRateModel:
    m = ResourceDropRateModel()
    m.item_code = drop_rate.code
    m.rate = drop_rate.rate
    m.min_quantity = drop_rate.min_quantity
    m.max_quantity = drop_rate.max_quantity
    return m


def resource_drop_to_schema(model: ResourceDropRateModel) -> DropRateSchema:
    return DropRateSchema(code=model.item_code,
                          rate=model.rate,
                          min_quantity=model.min_quantity,
                          max_quantity=model.max_quantity)


def resource_to_model(resource: ResourceSchema) -> ResourceModel:
    m = ResourceModel()
    m.code = resource.code
    m.name = resource.name
    m.level = resource.level
    m.skill = resource.skill
    m.drops = [resource_drop_to_model(drop) for drop in resource.drops]
    return m


def resource_to_schema(model: ResourceModel) -> ResourceSchema:
    return ResourceSchema(name=model.name,
                          code=model.code,
                          level=model.level,
                          skill=model.skill,
                          drops=[resource_drop_to_schema(drop)
                                 for drop in model.drops]
                          )
