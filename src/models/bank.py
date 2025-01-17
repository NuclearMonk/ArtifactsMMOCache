
from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base


class BankModel(Base):
    __tablename__ = 'banks'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slots: Mapped[int] 
    expansions: Mapped[int]
    next_expansion_cost: Mapped[int]
    gold: Mapped[int]
    dirty: Mapped[bool]