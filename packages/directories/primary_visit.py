from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.med.primary_visit import PrimaryVisitTable
from schemas.med.primary_visit import PrimaryVisitUpdateAttributes, PrimaryVisitInsertAttributes


async def get_primary_visits(db: AsyncSession, id: int = None):
    if id is None:
        query = await db.execute(
            select(PrimaryVisitTable)
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            dict = row.to_dict()

            disease_onset_date = dict.get('disease_onset_date')
            if disease_onset_date is not None:
                dict['disease_onset_date'] = disease_onset_date.isoformat()

            date_visit = dict.get('date_visit')
            if date_visit is not None:
                dict['date_visit'] = date_visit.isoformat()

            result.append(dict)
        return result

    query = await db.execute(
        select(PrimaryVisitTable).filter_by(id=id)
    )
    result = query.scalars().first()

    dict = result.to_dict()

    return dict if result else None


async def create_primary_visit(record: PrimaryVisitInsertAttributes, db: AsyncSession):
    formated_record = record.dict(include=record.__fields_set__)

    query = await db.execute(
        insert(PrimaryVisitTable).values(**formated_record)
    )

    # Отправляем в БД
    await db.commit()

    result = await db.execute(select(PrimaryVisitTable).filter_by(id=query.inserted_primary_key[0]))
    response = result.scalars().first()

    return response.to_dict()


async def delete_primary_visit(id: int, db: AsyncSession):
    # Выполняем запрос для нахождения записи по ID
    result = await db.execute(select(PrimaryVisitTable).filter_by(id=id))
    result = result.scalars().first()

    # Проверка, существует ли запись для удаления
    if result is None:
        return None

    # Удаляем запись
    await db.delete(result)
    await db.commit()

    dict = result.to_dict()

    date = dict.get('date')
    if date is not None:
        dict['date'] = date.isoformat()

    disease_onset_date = dict.get('disease_onset_date')
    if disease_onset_date is not None:
        dict['disease_onset_date'] = disease_onset_date.isoformat()

    # Возвращаем обновленный объект в виде словаря
    return dict if result else None


async def update_primary_visit(record: PrimaryVisitUpdateAttributes, db: AsyncSession):
    try:
        # Обновляем запись
        query = update(PrimaryVisitTable).where(PrimaryVisitTable.id == record.id).values(
            **record.dict(exclude_unset=True)
        )

        await db.execute(query)

        await db.commit()

        # Извлекаем обновленную запись
        result = await db.execute(select(PrimaryVisitTable).where(PrimaryVisitTable.id == record.id))
        result = result.scalars().first()

        dict = result.to_dict()

        # Возвращаем обновленный объект в виде словаря
        return dict if result else None

    except Exception as e:

        await db.rollback()  # Откат при ошибке
        raise e  # Бросаем исключение дальше

async def delete_primary_visit(id: int, db: AsyncSession):
    # Выполняем запрос для нахождения записи по ID
    result = await db.execute(select(PrimaryVisitTable).filter_by(id=id))
    result = result.scalars().first()

    # Проверка, существует ли запись для удаления
    if result is None:
        return None

    # Удаляем запись
    await db.delete(result)
    await db.commit()

    dict = result.to_dict()

    return dict
