from fastapi import HTTPException
from pydantic import Field
from pydantic import BaseModel, root_validator

"""Схема записи типа животного, для GET(получения)"""
class AnimalTypeGetAttributes(BaseModel):
    id: int = Field(...)
    name: str = Field(...)

"""Схема записи типа животного, для INSERT(создания)"""
class AnimalTypeInsertAttributes(BaseModel):
    name: str = Field(..., min_length=1, max_length=25)

"""Схема записи типа животного, для UPDATE(обновления)"""
class AnimalTypeUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., min_length=1, max_length=25)
