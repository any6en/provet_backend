from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from schemas.directories.animal_type import AnimalTypeInsertAttributes, AnimalTypeUpdateAttributes
from utils.responses import create_http_response, Http200, Http400
from packages.directories.animal_type import get_animal_types, create_animal_type, delete_animal_type, update_animal_type

# Роутер
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@worker.get("/animal_types", description="Получение списка записей")
async def get_route(id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_animal_types(db, id)
    if records is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    if id is None:
        return create_http_response(Http200({"records": len(records), "rows": records}))

    return create_http_response(Http200(records))


@worker.post("/animal_types/animal_type", description="Создание записи")
async def post_route(record: AnimalTypeInsertAttributes, db: AsyncSession = Depends(get_db)):
    try:
        new_record = await create_animal_type(record, db)
        return create_http_response(Http200(new_record))
    except Exception as e:
        return create_http_response(Http400(e.args))


@worker.delete("/animal_types/animal_type/{id}", description="Удаление записи по переданному Id")
async def delete_route(id: int, db: AsyncSession = Depends(get_db)):
    deleted_record = await delete_animal_type(id, db)
    if deleted_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(deleted_record))


@worker.patch("/animal_types/animal_type", description="Обновить запись по переданному Id")
async def update_route(record: AnimalTypeUpdateAttributes, db: AsyncSession = Depends(get_db)):
    updated_record = await update_animal_type(record, db)
    if updated_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(updated_record))
