from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from schemas.item import CraftSkill


class ItemEffectModel(Base):
    __tablename__ = 'item_effects'
    item_code : Mapped[str]= mapped_column(ForeignKey('items.code', ondelete='CASCADE'), primary_key=True)
    effect_name : Mapped[str]= mapped_column(primary_key=True)
    value: Mapped[int]


class CraftItemModel(Base):
    __tablename__ = 'craft_items'
    craft_code: Mapped[str] = mapped_column(
        ForeignKey('crafts.item_code', ondelete='Cascade'), primary_key=True)
    item_code: Mapped[str] = mapped_column(
        ForeignKey('items.code', ondelete='CASCADE'), primary_key=True)
    __table_args__ = (UniqueConstraint(craft_code, item_code),)
    quantity: Mapped[int]

    def __init__(self, item_code: str, quantity: int):
        super().__init__()
        self.item_code = item_code
        self.quantity = quantity


class CraftModel(Base):
    __tablename__ = 'crafts'
    item_code: Mapped[str] = mapped_column(
        ForeignKey('items.code', ondelete='CASCADE'), primary_key=True)
    skill: Mapped[CraftSkill | None] 
    level: Mapped[int | None]
    items: Mapped[list[CraftItemModel]] = relationship(uselist=True, cascade='all, delete')
    quantity: Mapped[int | None]


class ItemModel(Base):
    __tablename__ = 'items'
    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    level: Mapped[int]
    type: Mapped[str]
    subtype: Mapped[str]
    description: Mapped[str]
    effects: Mapped[list[ItemEffectModel]] = relationship(cascade='all,delete')
    craft: Mapped[CraftModel | None]  = relationship(cascade='all, delete')
    tradeable: Mapped[bool]
