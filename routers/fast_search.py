from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from packages.directories.breed import get_breeds
from utils.responses import create_http_response, Http200, Http400

# Роутер
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@worker.get("/patients", description="Получение списка записей")
async def get_route(id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_breeds(db, id)
    if records is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    if id is None:
        return create_http_response(Http200({"records": len(records), "rows": records}))

    return create_http_response(Http200(records))