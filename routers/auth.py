from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import AsyncSessionLocal
from packages.auth import get_auth_data
from schemas.user import LoginRequest

from utils.responses import create_http_response

# Роутер для авторизации пользователей
worker = APIRouter()

# Dependency for async DB sessions
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@worker.post("/login", description="Авторизация")
async def login(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    lol = await get_auth_data(db, login_request)
    return create_http_response(lol)
