

from models.bank import BankModel
from schemas.bank import BankSchema


def bank_to_schema(bank: BankModel)-> BankSchema:
    return BankSchema(slots=bank.slots, 
                      expansions= bank.expansions, 
                      next_expansion_cost=bank.next_expansion_cost,
                      gold = bank.gold)

