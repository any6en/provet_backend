from sqlalchemy import insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import logging

from models.med.repeat_visit import RepeatVisitTable
from schemas.med.repeat_visits import RepeatVisitInsertAttributes, RepeatVisitUpdateAttributes


async def get_repeat_visits(db: AsyncSession, id: int = None):
    if id is None:
        query = await db.execute(
            select(RepeatVisitTable)
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
        select(RepeatVisitTable).filter_by(id=id)
    )
    result = query.scalars().first()

    dict = result.to_dict()

    return dict if result else None


async def create_repeat_visit(record: RepeatVisitInsertAttributes, db: AsyncSession):
    formated_record = record.dict(include=record.__fields_set__)
    logging.info(record)
    logging.error(record)

    query = await db.execute(
        insert(RepeatVisitTable).values(**formated_record)
    )

    # Отправляем в БД
    await db.commit()

    result = await db.execute(select(RepeatVisitTable).filter_by(id=query.inserted_primary_key[0]))
    result = result.scalars().first()

    dict = result.to_dict()

    date_visit = dict.get('date_visit')
    if date_visit is not None:
        dict['date_visit'] = date_visit.isoformat()

    disease_onset_date = dict.get('disease_onset_date')
    if disease_onset_date is not None:
        dict['disease_onset_date'] = disease_onset_date.isoformat()

    return dict

async def update_repeat_visit(record: RepeatVisitUpdateAttributes, db: AsyncSession):
    try:
        # Обновляем запись
        query = update(RepeatVisitTable).where(RepeatVisitTable.id == record.id).values(
            **record.dict(exclude_unset=True)
        )

        await db.execute(query)

        await db.commit()

        # Извлекаем обновленную запись
        result = await db.execute(select(RepeatVisitTable).where(RepeatVisitTable.id == record.id))
        result = result.scalars().first()

        dict = result.to_dict()

        date_visit = dict.get('date_visit')
        if date_visit is not None:
            dict['date_visit'] = date_visit.isoformat()

        disease_onset_date = dict.get('disease_onset_date')
        if disease_onset_date is not None:
            dict['disease_onset_date'] = disease_onset_date.isoformat()

        # Возвращаем обновленный объект в виде словаря
        return dict if result else None
    except Exception as e:
        logging.info(e.args)
        logging.error(e.args)

        await db.rollback()  # Откат при ошибке
        raise e  # Бросаем исключение дальше

