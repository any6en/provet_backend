from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from packages.document_generator import get_document_primary_visit, get_pd_agreement_sign, get_document_repeat_visit
from schemas.directories.owner import OwnerAgreementSignPD

# Роутер
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Генерация проведенного первичного приема
@worker.get("/document_generator/primary_visit", description="Генерация документа")
async def get_route(primary_visit_id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_document_primary_visit(db, primary_visit_id)

    return records

# Генерация проведенного повторного приема
@worker.get("/document_generator/repeat_visit", description="Генерация документа")
async def get_route(repeat_visit_id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_document_repeat_visit(db, repeat_visit_id)

    return records

# Генерация договора об согласии на обработку персональных даннных
@worker.post("/document_generator/pd_agreement_sign", description="Генерация документа")
async def get_route(record: OwnerAgreementSignPD, db: AsyncSession = Depends(get_db)):
    records = await get_pd_agreement_sign(db, record)

    return records