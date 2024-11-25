from fastapi import HTTPException
from pydantic import BaseModel, root_validator, Field


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
    login: str = Field(...)
    password: str = Field(...)
