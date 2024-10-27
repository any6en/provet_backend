from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import logging
from database import AsyncSessionLocal
from packages.directories.primary_visit import get_primary_visits, create_primary_visit, delete_primary_visit, \
    update_primary_visit
from schemas.med.primary_visit import PrimaryVisitUpdateAttributes, PrimaryVisitInsertAttributes
from utils.responses import create_http_response, Http200, Http400

worker = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@worker.get("/primary_visits", description="Получение списка")
async def get_route(id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_primary_visits(db, id)
    if records is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    if id is None:
        return create_http_response(Http200({"records": len(records), "rows": records}))

    return create_http_response(Http200(records))

@worker.post("/primary_visits/primary_visit", description="Создание новой записи")
async def create_route(record: PrimaryVisitInsertAttributes, db: AsyncSession = Depends(get_db)):
    try:
        new_record = await create_primary_visit(record, db)
        return create_http_response(Http200(new_record))
    except Exception as e:
        logging.error(e.args)
        return create_http_response(Http400(e.args))

@worker.delete("/primary_visits/primary_visit/{id}", description="Удаление записи по переданному Id")
async def delete_route(id: int, db: AsyncSession = Depends(get_db)):
    deleted_record = await delete_primary_visit(id, db)
    if deleted_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(deleted_record))

@worker.patch("/primary_visits/primary_visit", description="Обновить информацию в записи")
async def update_route(record: PrimaryVisitUpdateAttributes, db: AsyncSession = Depends(get_db)):
    updated_record = await update_primary_visit(record, db)
    if updated_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(updated_record))