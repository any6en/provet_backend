from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from models.user import User
from schemas.user import LoginRequest
from fastapi.responses import JSONResponse

# Роутер для авторизации пользователей
auth_router = APIRouter(prefix="/auth", tags=["auth"])

# Dependency for async DB sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@auth_router.post("/login", response_model=None)
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

    result = await db.execute(select(User).where(User.login == login_request.login, User.password == login_request.password))
    user = result.scalars().first()

    # Если пользователь не найден, возвращаем ошибку
    if not user:
        return JSONResponse(
            status_code=400,
            content={"response": {"error": "Неверный логин или пароль"}}
        )

    # Возвращаем информацию о пользователе в формате, который вы хотите
    return JSONResponse(
        status_code=200,
        content={"response": user}
    )

