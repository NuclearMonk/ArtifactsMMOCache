
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base
from schemas.character import CharacterSkin


class InventorySlotModel(Base):
    __tablename__ = 'inventories'
    character_name: Mapped[str] = mapped_column(
        ForeignKey('characters.name'), primary_key=True)
    slot: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str| None] = mapped_column(ForeignKey('items.code'))
    quantity: Mapped[int]
    __table_args__ = (UniqueConstraint(character_name, slot),)


class CharacterModel(Base):
    __tablename__ = 'characters'
    name: Mapped[str] = mapped_column(primary_key=True)
    account: Mapped[str]
    skin: Mapped[CharacterSkin]
    level: Mapped[int]
    xp: Mapped[int]
    max_xp: Mapped[int]
    gold: Mapped[int]
    speed: Mapped[int]
    mining_level: Mapped[int]
    mining_xp: Mapped[int]
    mining_max_xp: Mapped[int]
    woodcutting_level: Mapped[int]
    woodcutting_xp: Mapped[int]
    woodcutting_max_xp: Mapped[int]
    fishing_level: Mapped[int]
    fishing_xp: Mapped[int]
    fishing_max_xp: Mapped[int]
    weaponcrafting_level: Mapped[int]
    weaponcrafting_xp: Mapped[int]
    weaponcrafting_max_xp: Mapped[int]
    gearcrafting_level: Mapped[int]
    gearcrafting_xp: Mapped[int]
    gearcrafting_max_xp: Mapped[int]
    jewelrycrafting_level: Mapped[int]
    jewelrycrafting_xp: Mapped[int]
    jewelrycrafting_max_xp: Mapped[int]
    cooking_level: Mapped[int]
    cooking_xp: Mapped[int]
    cooking_max_xp: Mapped[int]
    alchemy_level: Mapped[int]
    alchemy_xp: Mapped[int]
    alchemy_max_xp: Mapped[int]
    hp: Mapped[int]
    max_hp: Mapped[int]
    haste: Mapped[int]
    critical_strike: Mapped[int]
    stamina: Mapped[int]
    attack_fire: Mapped[int]
    attack_earth: Mapped[int]
    attack_water: Mapped[int]
    attack_air: Mapped[int]
    dmg_fire: Mapped[int]
    dmg_earth: Mapped[int]
    dmg_water: Mapped[int]
    dmg_air: Mapped[int]
    res_fire: Mapped[int]
    res_earth: Mapped[int]
    res_water: Mapped[int]
    res_air: Mapped[int]
    x: Mapped[int]
    y: Mapped[int]
    cooldown: Mapped[int]
    cooldown_expiration: Mapped[datetime] = mapped_column(DateTime(False))
    weapon_slot: Mapped[str]
    shield_slot: Mapped[str]
    helmet_slot: Mapped[str]
    body_armor_slot: Mapped[str]
    leg_armor_slot: Mapped[str]
    boots_slot: Mapped[str]
    ring1_slot: Mapped[str]
    ring2_slot: Mapped[str]
    amulet_slot: Mapped[str]
    artifact1_slot: Mapped[str]
    artifact2_slot: Mapped[str]
    artifact3_slot: Mapped[str]
    utility1_slot: Mapped[str]
    utility1_slot_quantity: Mapped[int]
    utility2_slot: Mapped[str]
    utility2_slot_quantity: Mapped[int]
    task: Mapped[str]
    task_type: Mapped[str]
    task_progress: Mapped[int]
    task_total: Mapped[int]
    inventory_max_items: Mapped[int]
    inventory: Mapped[list[InventorySlotModel]] = relationship()
