import logging
from datetime import datetime

from sqlalchemy import select, insert, delete, update, text
from sqlalchemy.ext.asyncio import AsyncSession
from models.owner import OwnerTable
from schemas.owner import OwnerInsertAttributes, OwnerUpdateAttributes


async def get_owners(db: AsyncSession, id: int = None):
    if id is None:
        query_rows = text("SELECT * FROM provet.owners;")
        result_rows = await db.execute(query_rows)
        rows = result_rows.all()

        result = []
        for row in rows:
            owner_dict = row._asdict()
            created_at = owner_dict.get('created_at')
            if created_at is not None:
                owner_dict['created_at'] = created_at.isoformat()

            date_birth = owner_dict.get('date_birth')
            if date_birth is not None:
                owner_dict['date_birth'] = date_birth.isoformat()

            result.append(owner_dict)
        return result

    query_rows = text("SELECT * FROM provet.owners WHERE id = :id")
    result_rows = await db.execute(query_rows, {"id": id})
    result_rows = result_rows.all()

    if result_rows is None:
        return None

    result = result_rows[0]._asdict()

    created_at = result.get('created_at')
    if created_at is not None:
        result['created_at'] = created_at.isoformat()

    date_birth = result.get('date_birth')
    if date_birth is not None:
        result['date_birth'] = date_birth.isoformat()

    return result

async def create_owner(owner: OwnerInsertAttributes, db: AsyncSession):
    owner_attrs = owner.dict(include=owner.__fields_set__)
    result = await db.execute(
        insert(OwnerTable).values(**owner_attrs)
    )
    new_owner_id = result.inserted_primary_key[0]
    new_owner_result = await db.execute(select(OwnerTable).filter_by(id=new_owner_id))
    new_owner = new_owner_result.scalars().first()

    new_owner_data = {
        "id": new_owner.id,
        "first_name": new_owner.first_name,
        "last_name": new_owner.last_name,
        "patronymic": new_owner.patronymic,
        "address": new_owner.address,
        "gender": new_owner.gender,
        "date_birth": new_owner.date_birth.isoformat() if new_owner.date_birth else None,
        "created_at": datetime.now().isoformat()
    }

    await db.flush()
    await db.commit()
    return new_owner_data

async def delete_owner(id: int, db: AsyncSession):
    result = await db.execute(select(OwnerTable).filter_by(id=id))
    owner = result.scalars().first()

    if owner is None:
        return None

    await db.delete(owner)
    await db.commit()
    deleted_owner_data = {
        "id": owner.id,
        "first_name": owner.first_name,
        "last_name": owner.last_name,
        "patronymic": owner.patronymic,
        "address": owner.address,
        "gender": owner.gender,
        "date_birth": owner.date_birth.isoformat() if owner.date_birth else None,
        "created_at": owner.created_at.isoformat(),
    }

    return deleted_owner_data

async def update_owner(updated_data: OwnerUpdateAttributes, db: AsyncSession):
    query = update(OwnerTable).where(OwnerTable.id == updated_data.id).values(**updated_data.dict(exclude_unset=True))
    await db.execute(query)
    await db.commit()
    updated_owner_result = await db.execute(select(OwnerTable).filter_by(id=updated_data.id))
    updated_owner = updated_owner_result.scalars().first()
    updated_owner_data = {
        "id": updated_owner.id,
        "first_name": updated_owner.first_name,
        "last_name": updated_owner.last_name,
        "patronymic": updated_owner.patronymic,
        "address": updated_owner.address,
        "gender": updated_owner.gender,
        "date_birth": updated_owner.date_birth.isoformat() if updated_owner.date_birth else None,
        "created_at": updated_owner.created_at.isoformat(),
    }
    return updated_owner_data