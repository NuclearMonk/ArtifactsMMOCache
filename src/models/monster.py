from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class MonsterDropRateModel(Base):
    __tablename__ = 'monster_drops'
    monster_code: Mapped[str] = mapped_column(ForeignKey(
        'monsters.code', ondelete='CASCADE'), primary_key=True)
    item_code: Mapped[str] = mapped_column(ForeignKey(
        'items.code', ondelete='CASCADE'), primary_key=True)
    rate: Mapped[int]
    min_quantity: Mapped[int]
    max_quantity: Mapped[int]


class MonsterModel(Base):
    __tablename__ = 'monsters'
    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    level: Mapped[int]
    hp: Mapped[int]
    attack_fire: Mapped[int]
    attack_earth: Mapped[int]
    attack_water: Mapped[int]
    attack_air: Mapped[int]
    res_fire: Mapped[int]
    res_earth: Mapped[int]
    res_water: Mapped[int]
    res_air: Mapped[int]
    min_gold: Mapped[int]
    max_gold: Mapped[int]
    drops: Mapped[list[MonsterDropRateModel]] = relationship(cascade='all,delete')
