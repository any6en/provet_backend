from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.directories.patient import PatientTable
from schemas.directories.patient import PatientInsertAttributes, PatientUpdateAttributes


async def get_patients(db: AsyncSession, id: int = None, owner_id: int = None):
    if owner_id is not None:
        query = await db.execute(
            select(PatientTable).options(selectinload(PatientTable.animal_type)).options(
                selectinload(PatientTable.breed)).filter_by(owner_id=owner_id)
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            result.append(row.to_dict_page())
        return result

    if id is None:
        query = await db.execute(
            select(PatientTable).options(selectinload(PatientTable.animal_type)).options(selectinload(PatientTable.breed))
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            result.append(row.to_dict_page())
        return result

    query = await db.execute(
        select(PatientTable).options(selectinload(PatientTable.animal_type)).options(selectinload(PatientTable.breed)).filter_by(id=id)
    )
    result = query.scalars().first()

    return result.to_dict_page() if result else None


async def create_patient(record: PatientInsertAttributes, db: AsyncSession):
    formated_record = record.dict(include=record.__fields_set__)

    query = await db.execute(
        insert(PatientTable).values(**formated_record)
    )

    # Отправляем в БД
    await db.commit()

    result = await db.execute(select(PatientTable).filter_by(id=query.inserted_primary_key[0]))
    result = result.scalars().first()

    return result.to_dict()


async def delete_patient(id: int, db: AsyncSession):
    # Выполняем запрос для нахождения записи по ID
    result = await db.execute(select(PatientTable).filter_by(id=id))
    result = result.scalars().first()

    # Проверка, существует ли запись для удаления
    if result is None:
        return None

    # Удаляем запись
    await db.delete(result)
    await db.commit()

    # Возвращаем обновленный объект в виде словаря
    return result.to_dict() if result else None


async def update_patient(record: PatientUpdateAttributes, db: AsyncSession):
    try:
        # Обновляем запись
        query = update(PatientTable).where(PatientTable.id == record.id).values(
            **record.dict(exclude_unset=True)
        )

        await db.execute(query)

        await db.commit()

        # Извлекаем обновленную запись
        result = await db.execute(select(PatientTable).where(PatientTable.id == record.id))
        result = result.scalars().first()

        # Возвращаем обновленный объект в виде словаря
        return result.to_dict() if result else None

    except Exception as e:
        await db.rollback()  # Откат при ошибке
        raise e  # Бросаем исключение дальше


async def get_patient_info(db: AsyncSession, id: int = None):
    if id is not None:
        query = await db.execute(
            select(PatientTable).options(selectinload(PatientTable.animal_type)).options(
                selectinload(PatientTable.breed)).filter_by(id=id)
        )
        return query.scalars().first().to_dict_info()
