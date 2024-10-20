from typing import Optional
from fastapi import HTTPException
from pydantic import BaseModel, Field, validator, root_validator


class BreedGetAttributes(BaseModel):
    """Атрибуты пород животных"""
    id: int = Field(...)
    name: str = Field(...)
    animal_type_id: int = Field(..., description="Идентификатор типа животного")

class BreedInsertAttributes(BaseModel):
    """Атрибуты для вставки пород животных"""
    name: str = Field(..., min_length=1, max_length=255, description="Название породы, от 1 до 255 символов")
    animal_type_id: int = Field(..., description="", validate_default=True)

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "animal_type_id" not in keys or not values.get("animal_type_id"):
            raise HTTPException(
                status_code=400,
                detail="Не указано какому виду принадлежит"
            )
        if "name" not in keys or not values.get("name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано название породы"
            )
        return values

class BreedUpdateAttributes(BaseModel):
    """Атрибуты для обновления пород животных"""
    id: int = Field(..., description="Идентификатор породы")
    name: Optional[str] = Field(None, min_length=1, max_length=255, description="Название породы, от 1 до 255 символов")
    animal_type_id: Optional[int] = Field(None, description="Идентификатор типа животного")

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "id" not in keys or not values.get("id"):
            raise HTTPException(
                status_code=400,
                detail="Не указано идентификатор породы"
            )
        return values
