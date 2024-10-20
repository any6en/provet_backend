from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession


from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from models.directories.patient import PatientTable
from schemas.directories.patient import PatientInsertAttributes, PatientUpdateAttributes


async def get_patients(db: AsyncSession, id: int = None):
    if id is None:
        query = await db.execute(
            select(PatientTable).options(selectinload(PatientTable.animal_type)).options(selectinload(PatientTable.breed))
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            dict = row.to_dict_page()

            date_birth = dict.get('date_birth')
            if date_birth is not None:
                dict['date_birth'] = date_birth.isoformat()

            created_at = dict.get('created_at')
            if created_at is not None:
                dict['created_at'] = created_at.isoformat()

            result.append(dict)
        return result

    query = await db.execute(
        select(PatientTable).options(selectinload(PatientTable.animal_type)).options(selectinload(PatientTable.breed))
    )
    result = query.scalars().first()

    dict = result.to_dict_page()

    date_birth = dict.get('date_birth')
    if date_birth is not None:
        dict['date_birth'] = date_birth.isoformat()

    created_at = dict.get('created_at')
    if created_at is not None:
        dict['created_at'] = created_at.isoformat()

    return dict if result else None


async def create_patient(record: PatientInsertAttributes, db: AsyncSession):
    formated_record = record.dict(include=record.__fields_set__)

    query = await db.execute(
        insert(PatientTable).values(**formated_record)
    )

    # Отправляем в БД
    await db.commit()

    result = await db.execute(select(PatientTable).filter_by(id=query.inserted_primary_key[0]))
    result = result.scalars().first()

    dict = result.to_dict()

    date_birth = dict.get('date_birth')
    if date_birth is not None:
        dict['date_birth'] = date_birth.isoformat()

    created_at = dict.get('created_at')
    if created_at is not None:
        dict['created_at'] = created_at.isoformat()

    return dict


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

    dict = result.to_dict()

    date_birth = dict.get('date_birth')
    if date_birth is not None:
        dict['date_birth'] = date_birth.isoformat()

    created_at = dict.get('created_at')
    if created_at is not None:
        dict['created_at'] = created_at.isoformat()

    # Возвращаем обновленный объект в виде словаря
    return dict if result else None


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

        dict = result.to_dict()

        date_birth = dict.get('date_birth')
        if date_birth is not None:
            dict['date_birth'] = date_birth.isoformat()

        created_at = dict.get('created_at')
        if created_at is not None:
            dict['created_at'] = created_at.isoformat()

        # Возвращаем обновленный объект в виде словаря
        return dict if result else None

    except Exception as e:
        await db.rollback()  # Откат при ошибке
        raise e  # Бросаем исключение дальше
