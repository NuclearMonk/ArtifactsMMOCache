

from datetime import datetime, timezone
from typing import Annotated
from fastapi import FastAPI, HTTPException
from fastapi import Request as FAPIRequest
from fastapi.params import Query
from sqlalchemy import and_, delete, or_, select
from converters.bank import bank_to_schema
from converters.item import item_to_model, item_to_schema
from converters.request import request_to_schema, response_to_schema
from environment import BASE_URL, ENGINE, get
from sqlalchemy.orm import Session

from models.bank import BankModel
from models.item import CraftItemModel, CraftModel, ItemModel, CraftSkill
from models.request import RequestModel
from schemas.item import ItemResponseSchema, ItemSchema, DataPageItemSchema
from schemas.request import Request, Response
from schemas.status import StatusResponseSchema
from schemas.account import AccountDetailsSchema, MyAccountDetails, MyAccountDetailsSchema
from schemas.bank import BankResponseSchema

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
        models = [item_to_model(item) for item in items]
        session.add_all(models)
        session.commit()
    return items


@app.get('/items')
def get_all_items(craft_material: str | None = None,
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
