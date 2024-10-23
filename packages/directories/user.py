from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import UserTable


async def get_users(db: AsyncSession, id: int = None):
    if id is None:
        query = await db.execute(
            select(UserTable)
        )
        rows = query.scalars().all()

        result = []
        for row in rows:
            dict = row.to_dict()

            result.append(dict)
        return result

    query = await db.execute(
        select(UserTable).filter_by(id=id)
    )
    result = query.scalars().first()

    dict = result.to_dict()

    return dict if result else None