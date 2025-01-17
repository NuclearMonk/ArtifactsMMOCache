from sqlalchemy import ForeignKey
from models.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from schemas.resource import GatheringSkill


class ResourceDropRateModel(Base):
    __tablename__ = 'resource_drops'
    resource_code: Mapped[str] = mapped_column(ForeignKey(
        'resources.code', ondelete='CASCADE'), primary_key=True)
    item_code: Mapped[str] = mapped_column(ForeignKey(
        'items.code', ondelete='CASCADE'), primary_key=True)
    rate: Mapped[int]
    min_quantity: Mapped[int]
    max_quantity: Mapped[int]


class ResourceModel(Base):
    __tablename__ = 'resources'
    code: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    skill: Mapped[GatheringSkill]
    level: Mapped[int]
    drops: Mapped[list[ResourceDropRateModel]
                  ] = relationship(cascade='all,delete')
