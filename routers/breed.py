from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from packages.breed import get_breeds, create_breed, delete_breed, update_breed
from schemas.breed import BreedInsertAttributes, BreedUpdateAttributes
from utils.responses import create_http_response, Http200, Http400

# Роутер
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@worker.get("/breeds", description="Получение списка записей")
async def get_route(id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_breeds(db, id)
    if records is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    if id is None:
        return create_http_response(Http200({"records": len(records), "rows": records}))

    return create_http_response(Http200(records))


@worker.post("/breeds/breed", description="Создание записи")
async def post_route(record: BreedInsertAttributes, db: AsyncSession = Depends(get_db)):
    try:
        new_record = await create_breed(record, db)
        return create_http_response(Http200(new_record))
    except Exception as e:
        return create_http_response(Http400(e.args))


@worker.delete("/breeds/breed/{id}", description="Удаление записи по переданному Id")
async def delete_route(id: int, db: AsyncSession = Depends(get_db)):
    record = await delete_breed(id, db)
    if record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(record))


@worker.patch("/breeds/breed", description="Обновить запись по переданному Id")
async def update_route(record: BreedUpdateAttributes, db: AsyncSession = Depends(get_db)):
    updated_record = await update_breed(record, db)
    if updated_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(updated_record))
