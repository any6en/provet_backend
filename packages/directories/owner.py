from datetime import datetime

from sqlalchemy import select, insert, update, text
from sqlalchemy.ext.asyncio import AsyncSession
from models.directories.owner import OwnerTable
from schemas.directories.owner import OwnerInsertAttributes, OwnerUpdateAttributes


async def get_owners(db: AsyncSession, id: int = None):
    # Если нужен весь справочник-
    if id is None:
        query = await db.execute(
            select(OwnerTable)
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            result.append(row.to_dict())
        return result
    # Если нужна только конкретная запись из справочника
    query = await db.execute(
        select(OwnerTable).filter_by(id=id)
    )
    result = query.scalars().first()

    dict = result.to_dict()

    return dict if result else None

async def create_owner(record: OwnerInsertAttributes, db: AsyncSession):
    formated_record = record.dict(include=record.__fields_set__)

    query = await db.execute(
        insert(OwnerTable).values(**formated_record)
    )

    # Отправляем в БД
    await db.commit()

    result = await db.execute(select(OwnerTable).filter_by(id=query.inserted_primary_key[0]))
    response = result.scalars().first()

    return response.to_dict()

async def delete_owner(id: int, db: AsyncSession):
    # Выполняем запрос для нахождения записи по ID
    result = await db.execute(select(OwnerTable).filter_by(id=id))
    result = result.scalars().first()

    # Проверка, существует ли запись для удаления
    if result is None:
        return None

    # Удаляем запись
    await db.delete(result)
    await db.commit()

    dict = result.to_dict()

    return dict

async def update_owner(record: OwnerUpdateAttributes, db: AsyncSession):
    try:
        # Обновляем запись
        query = update(OwnerTable).where(OwnerTable.id == record.id).values(
            **record.dict(exclude_unset=True)
        )

        await db.execute(query)

        await db.commit()

        # Извлекаем обновленную запись
        result = await db.execute(select(OwnerTable).where(OwnerTable.id == record.id))
        result = result.scalars().first()

        dict = result.to_dict()

        return dict if result else None

    except Exception as e:
        await db.rollback()
        raise e