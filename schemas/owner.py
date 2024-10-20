from typing import Optional

from fastapi import HTTPException
from pydantic import Field
from datetime import datetime
from pydantic import BaseModel, root_validator

class OwnerInsertAttributes(BaseModel):

    """Атрибуты владельцев"""
    first_name: str = Field(..., min_length=1, max_length=255, description="Имя, от 1 до 255 символов", validate_default=True)
    last_name: str = Field(..., min_length=1, max_length=255, description="Фамилия, от 1 до 255 символов", validate_default=True)
    patronymic: str = Field(..., min_length=1, max_length=255, description="Отчество, от 1 до 255 символов", validate_default=True)
    address: Optional[str] = None
    date_birth: Optional[datetime] = None
    gender: int = Field(..., ge=0, le=9, description="Пол: 0 - неизвестно, 1 - мужской, 2 - женский, 9 - неприменимо", validate_default=True)


    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "first_name" not in keys or not values.get("first_name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано имя"
            )
        if "last_name" not in keys or not values.get("last_name"):
            raise HTTPException(
                status_code=400,
                detail="Не указана фамилия"
            )
        if "patronymic" not in keys or not values.get("patronymic"):
            raise HTTPException(
                status_code=400,
                detail="Не указано отчество"
            )
        if "gender" not in keys or not values.get("gender"):
            raise HTTPException(
                status_code=400,
                detail="Не указан пол"
            )
        return values

    class Config:
        from_attributes = True

class OwnerUpdateAttributes(BaseModel):
    """Атрибуты владельцев"""
    id: int = Field(..., description="Идентификатор")

    first_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Имя, от 1 до 255 символов")
    last_name: Optional[str] = Field(None, min_length=1, max_length=255, description="Фамилия, от 1 до 255 символов")
    patronymic: Optional[str] = Field(None, min_length=1, max_length=255, description="Отчество, от 1 до 255 символов")
    address: Optional[str] = Field(None, max_length=255, description="Адрес, до 255 символов")  # Если нужно ограничение
    date_birth: Optional[datetime] = None
    gender: Optional[int] = Field(None, ge=0, le=9, description="Пол: 0 - неизвестно, 1 - мужской, 2 - женский, 9 - неприменимо")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "first_name" not in keys or not values.get("first_name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано имя"
            )
        if "last_name" not in keys or not values.get("last_name"):
            raise HTTPException(
                status_code=400,
                detail="Не указана фамилия"
            )
        if "patronymic" not in keys or not values.get("patronymic"):
            raise HTTPException(
                status_code=400,
                detail="Не указано отчество"
            )
        if "gender" not in keys or not values.get("gender"):
            raise HTTPException(
                status_code=400,
                detail="Не указан пол"
            )
        return values

    class Config:
        from_attributes = True