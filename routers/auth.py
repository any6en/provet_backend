from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models.user import UserTable
from schemas.user import LoginRequest
from fastapi.responses import JSONResponse

from utils.responses import create_http_response, Http200, Http400

# Роутер для авторизации пользователей
worker = APIRouter()

# Dependency for async DB sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@worker.post("/login", response_model=None)
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    """
    Обработчик авторизации пользователя.
    Принимает объект LoginRequest с полями login и password.
    Возвращает объект User, если логин и пароль верны.
    """
    # Проверяем, что пользователь ввел login и password
    if not login_request.login or not login_request.password:
        JSONResponse(
            status_code=400,
            content={"response": {"error": "Укажите логин и пароль"}}
        )

    # Аналогично, подгружаем animal_type, если id задан
    query = await db.execute(
        select(UserTable).where(UserTable.login == login_request.login,
                                UserTable.password == login_request.password))
    result = query.scalars().first()

    # Если пользователь не найден, возвращаем ошибку
    if not result:
        return create_http_response(Http400("Неверный логин или пароль"))

    # Возвращаем информацию о пользователе в формате, который вы хотите
    return create_http_response(Http200(result.to_dict()))

