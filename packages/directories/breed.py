from fastapi import HTTPException
from sqlalchemy import insert, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.directories.breed import BreedTable
from schemas.directories.breed import BreedUpdateAttributes, BreedInsertAttributes


from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

async def get_breeds(db: AsyncSession, id: int = None):
    if id is None:
        # Используем selectinload для подгрузки связанных объектов
        query = await db.execute(
            select(BreedTable).options(selectinload(BreedTable.animal_type))
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            result.append(row.to_dict_full())
        return result

    # Аналогично, подгружаем animal_type, если id задан
    query = await db.execute(
        select(BreedTable).options(selectinload(BreedTable.animal_type)).filter_by(id=id)
    )
    result = query.scalars().first()

    return result.to_dict_full() if result else None


async def create_breed(animal_type: BreedInsertAttributes, db: AsyncSession):
    try:
        animal_type_attrs = animal_type.dict(include=animal_type.__fields_set__)

        query = await db.execute(
            insert(BreedTable).values(**animal_type_attrs)
        )

        # Отправляем в БД
        await db.commit()

        result = await db.execute(select(BreedTable).filter_by(id=query.inserted_primary_key[0]))
        result = result.scalars().first()

        return result.to_dict()
    except IntegrityError:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Порода должна быть уникальной"
        )

async def delete_breed(id: int, db: AsyncSession):
    # Выполняем запрос для нахождения записи по ID
    result = await db.execute(select(BreedTable).filter_by(id=id))
    result = result.scalars().first()

    # Проверка, существует ли запись для удаления
    if result is None:
        return None

    # Удаляем запись
    await db.delete(result)
    await db.commit()

    # Возвращаем информацию об удаленной записи в формате словаря
    return result.to_dict()


async def update_breed(updated_data: BreedUpdateAttributes, db: AsyncSession):
    try:
        # Обновляем запись
        query = update(BreedTable).where(BreedTable.id == updated_data.id).values(
            **updated_data.dict(exclude_unset=True)
        )

        await db.execute(query)

        await db.commit()

        # Извлекаем обновленную запись
        updated_row = await db.execute(select(BreedTable).where(BreedTable.id == updated_data.id))
        updated_animal_type = updated_row.scalars().first()

        # Возвращаем обновленный объект в виде словаря
        return updated_animal_type.to_dict() if updated_animal_type else None

    except Exception as e:
        await db.rollback()  # Откат при ошибке
        raise e  # Бросаем исключение дальше
