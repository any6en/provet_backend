from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from packages.med.journal import get_journal, get_journal_visits
from utils.responses import create_http_response, Http200, Http400

# Роутер
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@worker.get("/journal", description="Получение списка ")
async def get_route(patient_id: int = None, db: AsyncSession = Depends(get_db)):
    if id is None:
        return create_http_response(Http400({"Требуется указать идентификатор пациента"}))

    records = await get_journal(db, patient_id)

    return create_http_response(Http200({"records": len(records), "rows": records}))

@worker.get("/journal_visits", description="Получение списка ")
async def get_route(primary_visit_id: int = None, db: AsyncSession = Depends(get_db)):
    if id is None:
        return create_http_response(Http400({"Требуется указать идентификатор первичного приема"}))

    records = await get_journal_visits(db, primary_visit_id)

    return create_http_response(Http200(records))
