

from fastapi import FastAPI, HTTPException
from sqlalchemy import and_, delete, func, select
from converters.bank import bank_item_to_schema, bank_to_schema
from converters.character import character_to_model, character_to_schema
from converters.item import item_to_model, item_to_schema
from converters.map import map_to_model, map_to_schema
from converters.monster import monster_to_model, monster_to_schema
from converters.request import request_to_schema
from converters.resource import resource_to_model, resource_to_schema
from environment import BASE_URL, ENGINE, get
from sqlalchemy.orm import Session

from models.bank import BankItemModel, BankModel
from models.character import CharacterModel
from models.item import CraftItemModel, CraftModel, ItemModel, CraftSkill
from models.map import MapModel
from models.monster import MonsterDropRateModel, MonsterModel
from models.request import RequestModel
from models.resource import ResourceDropRateModel, ResourceModel
from schemas.character import CharacterResponseSchema
from schemas.item import ItemResponseSchema, ItemSchema, DataPageItemSchema
from schemas.map import MapResponseSchema, MapSchema, DataPageMapSchema
from schemas.monster import DataPageMonsterSchema, MonsterResponseSchema, MonsterSchema
from schemas.request import Request
from schemas.resource import DataPageResourceSchema, GatheringSkill, ResourceResponseSchema, ResourceSchema
from schemas.status import StatusResponseSchema
from schemas.account import AccountDetailsSchema, MyAccountDetailsSchema
from schemas.bank import BankResponseSchema, DataPageBankItemSchema

app = FastAPI()


@app.get('/request/{id}/')
def get_request_data(id: int) -> Request:
    with Session(ENGINE) as session:
        if m := session.scalar(select(RequestModel).where(RequestModel.id == id)):
            return request_to_schema(m)
        raise HTTPException(status_code=404, detail=f'Request {id=} Not Found')


@app.get('/')
def get_status() -> StatusResponseSchema:
    resp = get(BASE_URL)
    return StatusResponseSchema.model_validate(resp.json())


@app.get('/my/details')
def get_my_account_details() -> MyAccountDetailsSchema:
    resp = get(BASE_URL+'/my/details/')
    return MyAccountDetailsSchema.model_validate(resp.json())


@app.get('/accounts/{username}')
def get_account_details(username: str) -> AccountDetailsSchema:
    resp = get(BASE_URL+f'/accounts/{username}')
    return AccountDetailsSchema.model_validate(resp.json())


@app.get('/my/bank')
def get_bank_details() -> BankResponseSchema:
    with Session(ENGINE) as session:
        if m := session.scalar(select(BankModel).where(BankModel.id == 0)):
            if not m.dirty:
                return BankResponseSchema(data=bank_to_schema(m))
        else:
            m = BankModel()
            m.id = 0
            session.add(m)
        resp = get(BASE_URL+f'/my/bank')
        b = BankResponseSchema.model_validate(resp.json()).data
        m.slots = b.slots
        m.expansions = b.expansions
        m.next_expansion_cost = b.next_expansion_cost
        m.gold = b.gold
        m.dirty = False
        session.commit()
        return BankResponseSchema(data=bank_to_schema(m))


@app.get('/my/bank/items')
def get_bank_items(item_code: str | None= None,
                   page: int = 1,
                   size: int = 50) -> DataPageBankItemSchema:
    with Session(ENGINE) as session:
        stmt = select(BankItemModel)
        if item_code:
            stmt = stmt.where(ItemModel.name == item_code)
        total = session.scalar(select(func.count()).select_from(stmt))
        stmt = stmt.limit(size).offset(page*size)
        return DataPageItemSchema(total=total, page=page, size=size, pages=(total//size)+1, data=[
            bank_item_to_schema(m) for m in session.scalars(stmt)])


@app.get('/items/{item_code}')
def get_item(item_code: str) -> ItemResponseSchema:
    with Session(ENGINE) as session:
        if m := session.scalar(select(ItemModel).where(ItemModel.code == item_code)):
            return ItemResponseSchema(data=item_to_schema(m))
        resp = get(BASE_URL+f'/items/{item_code}')
        if resp.ok:
            item = ItemResponseSchema.model_validate(resp.json()).data
            session.add(item_to_model(item))
            session.commit()
            return ItemResponseSchema(data=item)
        raise HTTPException(
            status_code=404, detail=f'Item {item_code=} Not Found')


@app.get('/cache/items/refresh')
def refresh_item_cache() -> list[ItemSchema]:
    page_size = 100
    page = 1
    items: list[ItemSchema] = []
    resp = get(BASE_URL + f'/items/', {'page': page, 'size': page_size})

    resp = DataPageItemSchema.model_validate(resp.json())
    items.extend(resp.data)
    while resp.page * page_size < resp.total:
        page = resp.page+1
        resp = get(BASE_URL + f'/items/', {'page': page, 'size': page_size})
        resp = DataPageItemSchema.model_validate(resp.json())
        items.extend(resp.data)
    with Session(ENGINE) as session:
        session.execute(delete(ItemModel))
        session.add_all(item_to_model(item) for item in items)
        session.commit()
    return items


@app.get('/cache/items')
def get_item_list(craft_material: str | None = None,
                  craft_skill: CraftSkill | None = None,
                  min_level: int | None = None,
                  max_level: int | None = None,
                  name: str | None = None,
                  type: str | None = None) -> list[ItemSchema]:
    with Session(ENGINE) as session:
        stmt = select(ItemModel)

        if min_level:
            stmt = stmt.where(ItemModel.level >= min_level)
        if max_level:
            stmt = stmt.where(ItemModel.level <= max_level)
        if name:
            stmt = stmt.where(ItemModel.name == name)
        if type:
            stmt = stmt.where(ItemModel.type == type)
        if craft_skill:
            stmt = stmt.join(CraftModel, ItemModel.craft).where(
                CraftModel.skill == craft_skill)
        if craft_material:
            stmt = stmt.join(CraftModel, ItemModel.craft).join(
                CraftItemModel, CraftModel.items).where(
                    CraftItemModel.item_code == craft_material
            )
        return [item_to_schema(m) for m in session.scalars(stmt)]


@app.get('/items')
def get_all_items(craft_material: str | None = None,
                  craft_skill: CraftSkill | None = None,
                  min_level: int | None = None,
                  max_level: int | None = None,
                  name: str | None = None,
                  type: str | None = None,
                  page: int = 1,
                  size: int = 50) -> DataPageItemSchema:
    with Session(ENGINE) as session:
        stmt = select(ItemModel)

        if min_level:
            stmt = stmt.where(ItemModel.level >= min_level)
        if max_level:
            stmt = stmt.where(ItemModel.level <= max_level)
        if name:
            stmt = stmt.where(ItemModel.name == name)
        if type:
            stmt = stmt.where(ItemModel.type == type)
        if craft_skill:
            stmt = stmt.join(CraftModel, ItemModel.craft).where(
                CraftModel.skill == craft_skill)
        if craft_material:
            stmt = stmt.join(CraftModel, ItemModel.craft).join(
                CraftItemModel, CraftModel.items).where(
                    CraftItemModel.item_code == craft_material
            )
        total = session.scalar(select(func.count()).select_from(stmt))
        stmt = stmt.limit(size).offset(page*size)

        return DataPageItemSchema(total=total, page=page, size=size, pages=(total//size)+1, data=[
            item_to_schema(m) for m in session.scalars(stmt)])


@app.get('/cache/monsters/refresh')
def refresh_monster_cache() -> list[MonsterSchema]:
    page_size = 100
    page = 1
    monsters: list[MonsterSchema] = []
    resp = get(BASE_URL + f'/monsters/', {'page': page, 'size': page_size})

    resp = DataPageMonsterSchema.model_validate(resp.json())
    monsters.extend(resp.data)
    while resp.page * page_size < resp.total:
        page = resp.page+1
        resp = get(BASE_URL + f'/items/', {'page': page, 'size': page_size})
        resp = DataPageMonsterSchema.model_validate(resp.json())
        monsters.extend(resp.data)
    with Session(ENGINE) as session:
        session.execute(delete(MonsterModel))
        session.add_all(monster_to_model(monster) for monster in monsters)
        session.commit()
    return monsters


@app.get('/cache/monsters')
def get_monsters_list(drop: str | None = None,
                      min_level: int | None = None,
                      max_level: int | None = None,) -> list[MonsterSchema]:
    with Session(ENGINE) as session:
        stmt = select(MonsterModel)
        if min_level:
            stmt = stmt.where(MonsterModel.level >= min_level)
        if max_level:
            stmt = stmt.where(MonsterModel.level <= max_level)
        if drop:
            stmt = stmt.join(MonsterDropRateModel, MonsterModel.drops).where(
                MonsterDropRateModel.item_code == drop)
        return [monster_to_schema(m) for m in session.scalars(stmt)]


@app.get('/monsters/{monster_code}')
def get_monsters(monster_code: str) -> MonsterResponseSchema:
    with Session(ENGINE) as session:
        if m := session.scalar(select(MonsterModel).where(MonsterModel.code == monster_code)):
            return MonsterResponseSchema(data=monster_to_schema(m))
        resp = get(BASE_URL+f'/monsters/{monster_code}')
        if resp.ok:
            monster = MonsterResponseSchema.model_validate(resp.json()).data
            session.add(monster_to_model(monster))
            session.commit()
            return MonsterResponseSchema(data=monster)
        raise HTTPException(
            status_code=404, detail=f'Monster {monster_code=} Not Found')


@app.get('/monsters')
def get_all_monsters(drop: str | None = None,
                     min_level: int | None = None,
                     max_level: int | None = None,
                     page: int = 1,
                     size: int = 50) -> DataPageMonsterSchema:
    with Session(ENGINE) as session:
        stmt = select(MonsterModel)
        if min_level:
            stmt = stmt.where(MonsterModel.level >= min_level)
        if max_level:
            stmt = stmt.where(MonsterModel.level <= max_level)
        if drop:
            stmt = stmt.join(MonsterDropRateModel, MonsterModel.drops).where(
                MonsterDropRateModel.item_code == drop)
        total = session.scalar(select(func.count()).select_from(stmt))
        stmt = stmt.limit(size).offset(page*size)
        return DataPageMonsterSchema(total=total, page=page, size=size, pages=(total//size)+1, data=[
            monster_to_schema(m) for m in session.scalars(stmt)])


@app.get('/cache/resources/refresh')
def refresh_resource_cache() -> list[ResourceSchema]:
    page_size = 100
    page = 1
    resources: list[ResourceSchema] = []
    resp = get(BASE_URL + f'/resources/', {'page': page, 'size': page_size})

    resp = DataPageResourceSchema.model_validate(resp.json())
    resources.extend(resp.data)
    while resp.page * page_size < resp.total:
        page = resp.page+1
        resp = get(BASE_URL + f'/items/', {'page': page, 'size': page_size})
        resp = DataPageResourceSchema.model_validate(resp.json())
        resources.extend(resp.data)
    with Session(ENGINE) as session:
        session.execute(delete(ResourceModel))
        session.add_all(resource_to_model(resource) for resource in resources)
        session.commit()
    return resources


@app.get('/cache/resources')
def get_resources_list(drop: str | None = None,
                       skill: GatheringSkill = None,
                       min_level: int | None = None,
                       max_level: int | None = None) -> list[ResourceSchema]:
    with Session(ENGINE) as session:
        stmt = select(ResourceModel)
        if min_level:
            stmt = stmt.where(ResourceModel.level >= min_level)
        if max_level:
            stmt = stmt.where(ResourceModel.level <= max_level)
        if skill:
            stmt = stmt.where(ResourceModel.skill == skill)
        if drop:
            stmt = stmt.join(ResourceDropRateModel, ResourceModel.drops).where(
                ResourceDropRateModel.item_code == drop)
        return [resource_to_schema(m) for m in session.scalars(stmt)]


@app.get('/resources/{resource_code}')
def get_resources(resource_code: str) -> ResourceResponseSchema:
    with Session(ENGINE) as session:
        if m := session.scalar(select(ResourceModel).where(ResourceModel.code == resource_code)):
            return ResourceResponseSchema(data=resource_to_schema(m))
        resp = get(BASE_URL+f'/resources/{resource_code}')
        if resp.ok:
            resource = ResourceResponseSchema.model_validate(resp.json()).data
            session.add(resource_to_model(resource))
            session.commit()
            return ResourceResponseSchema(data=resource)
        raise HTTPException(
            status_code=404, detail=f'Resource {resource_code=} Not Found')


@app.get('/resources')
def get_all_resources(drop: str | None = None,
                      skill: GatheringSkill = None,
                      min_level: int | None = None,
                      max_level: int | None = None,
                      page: int = 1,
                      size: int = 50) -> DataPageResourceSchema:
    with Session(ENGINE) as session:
        stmt = select(ResourceModel)
        if min_level:
            stmt = stmt.where(ResourceModel.level >= min_level)
        if max_level:
            stmt = stmt.where(ResourceModel.level <= max_level)
        if skill:
            stmt = stmt.where(ResourceModel.skill == skill)
        if drop:
            stmt = stmt.join(ResourceDropRateModel, ResourceModel.drops).where(
                ResourceDropRateModel.item_code == drop)
        total = session.scalar(select(func.count()).select_from(stmt))
        stmt = stmt.limit(size).offset(page*size)
        return DataPageResourceSchema(total=total, page=page, size=size, pages=(total//size)+1, data=[
            resource_to_schema(m) for m in session.scalars(stmt)])


@app.get('/cache/maps/refresh')
def refresh_maps_cache() -> list[MapSchema]:
    page_size = 100
    page = 1
    maps: list[MapSchema] = []
    resp = get(BASE_URL + f'/maps/', {'page': page, 'size': page_size})

    resp = DataPageMapSchema.model_validate(resp.json())
    maps.extend(resp.data)
    while resp.page * page_size < resp.total:
        page = resp.page+1
        resp = get(BASE_URL + f'/maps/', {'page': page, 'size': page_size})
        resp = DataPageMapSchema.model_validate(resp.json())
        maps.extend(resp.data)
    with Session(ENGINE) as session:
        session.execute(delete(MapModel))
        session.add_all(map_to_model(map) for map in maps)
        session.commit()
    return maps


@app.get('/maps/{x}/{y}')
def get_maps(x: int, y: int) -> MapResponseSchema:
    with Session(ENGINE) as session:
        if m := session.scalar(select(MapModel).where(and_(MapModel.x == x, MapModel.y == y))):
            return MapResponseSchema(data=map_to_schema(m))
        resp = get(BASE_URL+f'/maps/{x}/{y}')
        if resp.ok:
            map = MapResponseSchema.model_validate(resp.json()).data
            session.add(map_to_model(map))
            session.commit()
            return MapResponseSchema(data=map)
        raise HTTPException(
            status_code=404, detail=f'Map ({x=} {y=}) Not Found')


@app.get('/maps')
def get_maps_list(content_code: str | None = None,
                 content_type: str | None = None,
                 page: int = 1,
                 size: int = 50) -> DataPageMapSchema:
    with Session(ENGINE) as session:
        stmt = select(MapModel)
        if content_code:
            stmt = stmt.where(MapModel.content_code == content_code)
        if content_type:
            stmt = stmt.where(MapModel.content_type == content_type)
        total = session.scalar(select(func.count()).select_from(stmt))
        stmt = stmt.limit(size).offset(page*size)

        return DataPageMapSchema(total=total, page=page, size=size, pages=(total//size)+1, data=[map_to_schema(m) for m in session.scalars(stmt)])


@app.get('/cache/maps')
def get_maps_list(content_code: str | None = None,
                 content_type: str | None = None) -> list[MapSchema]:
    with Session(ENGINE) as session:
        stmt = select(MapModel)
        if content_code:
            stmt = stmt.where(MapModel.content_code == content_code)
        if content_type:
            stmt = stmt.where(MapModel.content_type == content_type)
        return [map_to_schema(m) for m in session.scalars(stmt)]


@app.get('/characters/{name}')
def get_characters(name: str) -> CharacterResponseSchema:
    with Session(ENGINE) as session:
        if m := session.scalar(select(CharacterModel).where(CharacterModel.name == name)):
            return CharacterResponseSchema(data=character_to_schema(m))
        resp = get(BASE_URL+f'/characters/{name}')
        if resp.ok:
            character = CharacterResponseSchema.model_validate(resp.json()).data
            session.add(character_to_model(character))
            session.commit()
            return CharacterResponseSchema(data=character)
        raise HTTPException(
            status_code=404, detail=f'Character {name=} Not Found')