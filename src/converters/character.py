

from models.character import CharacterModel, InventorySlotModel
from schemas.character import CharacterSchema, InventorySlotSchema


def inventory_slot_to_model(inventory_slot: InventorySlotSchema) -> InventorySlotModel:
    m = InventorySlotModel()
    m.slot = inventory_slot.slot
    m.code = inventory_slot.code if inventory_slot.code else None
    m.quantity = inventory_slot.quantity 
    return m


def inventory_slot_to_schema(model: InventorySlotModel) -> InventorySlotSchema:
    return InventorySlotSchema(slot=model.slot,
                               code=model.code if model.code else '',
                               quantity=model.quantity)


def character_to_model(character: CharacterSchema) -> CharacterModel:
    m = CharacterModel()
    m.name = character.name
    m.account = character.account
    m.skin = character.skin
    m.level = character.level
    m.xp = character.xp
    m.max_xp = character.max_xp
    m.gold = character.gold
    m.speed = character.speed
    m.mining_level = character.mining_level
    m.mining_xp = character.mining_xp
    m.mining_max_xp = character.mining_max_xp
    m.woodcutting_level = character.woodcutting_level
    m.woodcutting_xp = character.woodcutting_xp
    m.woodcutting_max_xp = character.woodcutting_max_xp
    m.fishing_level = character.fishing_level
    m.fishing_xp = character.fishing_xp
    m.fishing_max_xp = character.fishing_max_xp
    m.weaponcrafting_level = character.weaponcrafting_level
    m.weaponcrafting_xp = character.weaponcrafting_xp
    m.weaponcrafting_max_xp = character.weaponcrafting_max_xp
    m.gearcrafting_level = character.gearcrafting_level
    m.gearcrafting_xp = character.gearcrafting_xp
    m.gearcrafting_max_xp = character.gearcrafting_max_xp
    m.jewelrycrafting_level = character.jewelrycrafting_level
    m.jewelrycrafting_xp = character.jewelrycrafting_xp
    m.jewelrycrafting_max_xp = character.jewelrycrafting_max_xp
    m.cooking_level = character.cooking_level
    m.cooking_xp = character.cooking_xp
    m.cooking_max_xp = character.cooking_max_xp
    m.alchemy_level = character.alchemy_level
    m.alchemy_xp = character.alchemy_xp
    m.alchemy_max_xp = character.alchemy_max_xp
    m.hp = character.hp
    m.max_hp = character.max_hp
    m.haste = character.haste
    m.critical_strike = character.critical_strike
    m.stamina = character.stamina
    m.attack_fire = character.attack_fire
    m.attack_earth = character.attack_earth
    m.attack_water = character.attack_water
    m.attack_air = character.attack_air
    m.dmg_fire = character.dmg_fire
    m.dmg_earth = character.dmg_earth
    m.dmg_water = character.dmg_water
    m.dmg_air = character.dmg_air
    m.res_fire = character.res_fire
    m.res_earth = character.res_earth
    m.res_water = character.res_water
    m.res_air = character.res_air
    m.x = character.x
    m.y = character.y
    m.cooldown = character.cooldown
    m.cooldown_expiration = character.cooldown_expiration
    m.weapon_slot = character.weapon_slot
    m.shield_slot = character.shield_slot
    m.helmet_slot = character.helmet_slot
    m.body_armor_slot = character.body_armor_slot
    m.leg_armor_slot = character.leg_armor_slot
    m.boots_slot = character.boots_slot
    m.ring1_slot = character.ring1_slot
    m.ring2_slot = character.ring2_slot
    m.amulet_slot = character.amulet_slot
    m.artifact1_slot = character.artifact1_slot
    m.artifact2_slot = character.artifact2_slot
    m.artifact3_slot = character.artifact3_slot
    m.utility1_slot = character.utility1_slot
    m.utility1_slot_quantity = character.utility1_slot_quantity
    m.utility2_slot = character.utility2_slot
    m.utility2_slot_quantity = character.utility2_slot_quantity
    m.task = character.task
    m.task_type = character.task_type
    m.task_progress = character.task_progress
    m.task_total = character.task_total
    m.inventory_max_items = character.inventory_max_items
    m.inventory = [inventory_slot_to_model(
        inventory_slot) for inventory_slot in character.inventory]
    return m


def character_to_schema(model: CharacterModel) -> CharacterSchema:
    return CharacterSchema(name=model.name,
                           account=model.account,
                           skin=model.skin,
                           level=model.level,
                           xp=model.xp,
                           max_xp=model.max_xp,
                           gold=model.gold,
                           speed=model.speed,
                           mining_level=model.mining_level,
                           mining_xp=model.mining_xp,
                           mining_max_xp=model.mining_max_xp,
                           woodcutting_level=model.woodcutting_level,
                           woodcutting_xp=model.woodcutting_xp,
                           woodcutting_max_xp=model.woodcutting_max_xp,
                           fishing_level=model.fishing_level,
                           fishing_xp=model.fishing_xp,
                           fishing_max_xp=model.fishing_max_xp,
                           weaponcrafting_level=model.weaponcrafting_level,
                           weaponcrafting_xp=model.weaponcrafting_xp,
                           weaponcrafting_max_xp=model.weaponcrafting_max_xp,
                           gearcrafting_level=model.gearcrafting_level,
                           gearcrafting_xp=model.gearcrafting_xp,
                           gearcrafting_max_xp=model.gearcrafting_max_xp,
                           jewelrycrafting_level=model.jewelrycrafting_level,
                           jewelrycrafting_xp=model.jewelrycrafting_xp,
                           jewelrycrafting_max_xp=model.jewelrycrafting_max_xp,
                           cooking_level=model.cooking_level,
                           cooking_xp=model.cooking_xp,
                           cooking_max_xp=model.cooking_max_xp,
                           alchemy_level=model.alchemy_level,
                           alchemy_xp=model.alchemy_xp,
                           alchemy_max_xp=model.alchemy_max_xp,
                           hp=model.hp,
                           max_hp=model.max_hp,
                           haste=model.haste,
                           critical_strike=model.critical_strike,
                           stamina=model.stamina,
                           attack_fire=model.attack_fire,
                           attack_earth=model.attack_earth,
                           attack_water=model.attack_water,
                           attack_air=model.attack_air,
                           dmg_fire=model.dmg_fire,
                           dmg_earth=model.dmg_earth,
                           dmg_water=model.dmg_water,
                           dmg_air=model.dmg_air,
                           res_fire=model.res_fire,
                           res_earth=model.res_earth,
                           res_water=model.res_water,
                           res_air=model.res_air,
                           x=model.x,
                           y=model.y,
                           cooldown=model.cooldown,
                           cooldown_expiration=model.cooldown_expiration,
                           weapon_slot=model.weapon_slot,
                           shield_slot=model.shield_slot,
                           helmet_slot=model.helmet_slot,
                           body_armor_slot=model.body_armor_slot,
                           leg_armor_slot=model.leg_armor_slot,
                           boots_slot=model.boots_slot,
                           ring1_slot=model.ring1_slot,
                           ring2_slot=model.ring2_slot,
                           amulet_slot=model.amulet_slot,
                           artifact1_slot=model.artifact1_slot,
                           artifact2_slot=model.artifact2_slot,
                           artifact3_slot=model.artifact3_slot,
                           utility1_slot=model.utility1_slot,
                           utility1_slot_quantity=model.utility1_slot_quantity,
                           utility2_slot=model.utility2_slot,
                           utility2_slot_quantity=model.utility2_slot_quantity,
                           task=model.task,
                           task_type=model.task_type,
                           task_progress=model.task_progress,
                           task_total=model.task_total,
                           inventory_max_items=model.inventory_max_items,
                           inventory=[inventory_slot_to_schema(inventory_slot) for inventory_slot in model.inventory ])
