from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import logging
from database import AsyncSessionLocal
from schemas.directories.owner import OwnerInsertAttributes, OwnerUpdateAttributes
from utils.responses import create_http_response, Http200, Http400
from packages.directories.owner import get_owners, create_owner, delete_owner, update_owner

# Роутер для владельцев
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@worker.get("/owners", description="Получение списка владельцев")
async def get_route(id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_owners(db, id)
    if records is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    if id is None:
        return create_http_response(Http200({"records": len(records), "rows": records}))

    return create_http_response(Http200(records))

@worker.post("/owners/owner", description="Создание нового владельца")
async def create_route(record: OwnerInsertAttributes, db: AsyncSession = Depends(get_db)):
    try:
        new_record = await create_owner(record, db)
        return create_http_response(Http200(new_record))
    except Exception as e:
        logging.error(e.args)
        return create_http_response(Http400(e.args))

@worker.delete("/owners/owner/{id}", description="Удаление владельца по переданному Id")
async def delete_route(id: int, db: AsyncSession = Depends(get_db)):
    deleted_record = await delete_owner(id, db)
    if deleted_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(deleted_record))

@worker.patch("/owners/owner", description="Обновить информацию в записи")
async def update_route(record: OwnerUpdateAttributes, db: AsyncSession = Depends(get_db)):
    updated_record = await update_owner(record, db)
    if updated_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(updated_record))