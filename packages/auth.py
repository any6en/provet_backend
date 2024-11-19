from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import UserTable
from schemas.user import LoginRequest
from utils.responses import Http400, Http200

# Обработка авторизации
async def get_auth_data(db: AsyncSession, login_request: LoginRequest):
    query = await db.execute(
        select(UserTable).where(UserTable.login == login_request.login,
            UserTable.password == login_request.password))
    result = query.scalars().first()

    # Если пользователь не найден
    if not result:
        return Http400("Неверно введены данные")

    # Возвращаем найденную запись в виде словаря
    return Http200(result.to_dict())