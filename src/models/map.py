
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class MapModel(Base):
    __tablename__ = 'maps'
    x: Mapped[int] = mapped_column(primary_key=True)
    y: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    skin: Mapped[str]
    content_type: Mapped[str | None]
    content_code: Mapped[str | None]
    __table_args__ = (UniqueConstraint(x, y),)
