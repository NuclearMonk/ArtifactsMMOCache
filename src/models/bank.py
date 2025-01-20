
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class BankModel(Base):
    __tablename__ = 'banks'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slots: Mapped[int]
    expansions: Mapped[int]
    next_expansion_cost: Mapped[int]
    gold: Mapped[int]
    dirty: Mapped[bool]


class BankItemModel(Base):
    __tablename__ = 'bank_items'
    item_code: Mapped[str] = mapped_column(
        ForeignKey('items.code'), primary_key=True)
    quantity: Mapped[int]
