from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession
from models.directories.animal_type import AnimalTypeTable
from schemas.directories.animal_type import AnimalTypeInsertAttributes, AnimalTypeUpdateAttributes


async def get_animal_types(db: AsyncSession, id: int = None):
    if id is None:
        query = await db.execute(select(AnimalTypeTable))
        rows = query.scalars().all()

        result = []
        for row in rows:
            result.append(row.to_dict())
        return result

    query = await db.execute(select(AnimalTypeTable).filter_by(id=id))
    result = query.scalars().first()

    return result.to_dict()


async def create_animal_type(animal_type: AnimalTypeInsertAttributes, db: AsyncSession):
    animal_type_attrs = animal_type.dict(include=animal_type.__fields_set__)

    query = await db.execute(
        insert(AnimalTypeTable).values(**animal_type_attrs)
    )

    # Отправляем в БД
    await db.commit()

    result = await db.execute(select(AnimalTypeTable).filter_by(id=query.inserted_primary_key[0]))
    result = result.scalars().first()

    return result.to_dict()


async def delete_animal_type(id: int, db: AsyncSession):
    # Выполняем запрос для нахождения записи по ID
    result = await db.execute(select(AnimalTypeTable).filter_by(id=id))
    result = result.scalars().first()

    # Проверка, существует ли запись для удаления
    if result is None:
        return None

    # Удаляем запись
    await db.delete(result)
    await db.commit()

    # Возвращаем информацию об удаленной записи в формате словаря
    return result.to_dict()


async def update_animal_type(updated_data: AnimalTypeUpdateAttributes, db: AsyncSession):
    try:
        # Обновляем запись
        query = update(AnimalTypeTable).where(AnimalTypeTable.id == updated_data.id).values(
            **updated_data.dict(exclude_unset=True)
        )

        await db.execute(query)

        await db.commit()

        # Извлекаем обновленную запись
        updated_row = await db.execute(select(AnimalTypeTable).where(AnimalTypeTable.id == updated_data.id))
        updated_animal_type = updated_row.scalars().first()

        # Возвращаем обновленный объект в виде словаря
        return updated_animal_type.to_dict() if updated_animal_type else None

    except Exception as e:
        await db.rollback()  # Откат при ошибке
        raise e  # Бросаем исключение дальше
