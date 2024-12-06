from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import AsyncSessionLocal
from schemas.directories.patient import PatientInsertAttributes, PatientUpdateAttributes
from utils.responses import create_http_response, Http200, Http400
from packages.directories.patient import get_patients, create_patient, delete_patient, update_patient, get_patient_info

# Роутер для владельцев
worker = APIRouter()


# Зависимость для асинхронных сеансов работы с базой данных
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@worker.get("/patients", description="Получение списка пациентов")
async def get_route(id: int = None, owner_id: int = None, db: AsyncSession = Depends(get_db)):
    records = await get_patients(db, id, owner_id)
    if records is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    if id is None:
        return create_http_response(Http200({"records": len(records), "rows": records}))

    return create_http_response(Http200(records))

@worker.post("/patients/patient", description="Создание новой записи")
async def create_route(record: PatientInsertAttributes, db: AsyncSession = Depends(get_db)):
    try:
        new_record = await create_patient(record, db)
        return create_http_response(Http200(new_record))
    except Exception as e:
        return create_http_response(Http400(e.args))

@worker.delete("/patients/patient/{id}", description="Удаление записи по переданному Id")
async def delete_route(id: int, db: AsyncSession = Depends(get_db)):
    deleted_record = await delete_patient(id, db)
    if deleted_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(deleted_record))

@worker.patch("/patients/patient", description="Обновить информацию в записи")
async def update_route(record: PatientUpdateAttributes, db: AsyncSession = Depends(get_db)):
    updated_record = await update_patient(record, db)
    if updated_record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(updated_record))

@worker.get("/patients/patient/info", description="Получение информации")
async def get_route(id: int = None, db: AsyncSession = Depends(get_db)):
    if id is None:
        return create_http_response(Http200("Идентификатор обязателен"))

    record = await get_patient_info(db, id)
    if record is None:
        return create_http_response(Http400({"error": "Такой записи не существует"}))

    return create_http_response(Http200(record))