

from models.bank import BankItemModel, BankModel
from schemas.bank import BankSchema
from schemas.item import SimpleItemSchema


def bank_to_schema(bank: BankModel) -> BankSchema:
    return BankSchema(slots=bank.slots,
                      expansions=bank.expansions,
                      next_expansion_cost=bank.next_expansion_cost,
                      gold=bank.gold)


def bank_item_to_schema(model: BankItemModel) -> SimpleItemSchema:
    return SimpleItemSchema(code=model.item_code, quantity=model.quantity)


def bank_item_to_model(item: SimpleItemSchema) -> BankItemModel:
    m = BankItemModel()
    m.item_code = item.code
    m.quantity = item.quantity
    return m
