from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from packages.document_generator import get_consent_processing_personal_data, get_document_primary_visit, \
    get_document_repeat_visit

# Роутер
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@worker.get("/document_generator/primary_visit", description="Генерация документа")
async def get_route(primary_visit_id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_document_primary_visit(db, primary_visit_id)

    return records

@worker.get("/document_generator/repeat_visit", description="Генерация документа")
async def get_route(repeat_visit_id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_document_repeat_visit(db, repeat_visit_id)

    return records

@worker.get("/document_generator/consent_processing_personal_data", description="Генерация документа")
async def get_route(primary_visit_id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_consent_processing_personal_data(db, primary_visit_id)

    return records