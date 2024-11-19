from fastapi import HTTPException
from pydantic import BaseModel, root_validator, Field
import logging


class User(BaseModel):
    id: int
    login: str
    email: str
    first_name: str
    last_name: str
    patronymic: str
    avatar: str
    password: str
    role: str
    class Config:
        from_attributes = True


class LoginRequest(BaseModel):
    login: str = Field(..., description="Логин")
    password: str = Field(..., description="Пароль")
    logging.error(login)
    logging.error(password)

    @root_validator(pre=True)
    def validate_ids(cls, values):
        keys = values.keys()

        if "login" not in keys or values.get("login") is None:
            raise HTTPException(status_code=400, detail="Не указан логин")
        if "password" not in keys or values.get("password") is None:
            raise HTTPException(status_code=400, detail="Не указан пароль")