from fastapi import HTTPException
from pydantic import Field
from pydantic import BaseModel, root_validator

"""Схема записи типа животного, для GET(получения)"""
class AnimalTypeGetAttributes(BaseModel):
    id: int = Field(...)
    name: str = Field(...)


"""Схема записи типа животного, для INSERT(создания)"""
class AnimalTypeInsertAttributes(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Название", validate_default=True)

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "name" not in keys or not values.get("name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано название"
            )
        return values

"""Схема записи типа животного, для UPDATE(обновления)"""
class AnimalTypeUpdateAttributes(BaseModel):
    id: int = Field(..., description="Идентификатор")
    name: str = Field(..., min_length=1, max_length=255, description="Название", validate_default=True)

    @root_validator(pre=True)
    def pre_validator(cls, values):
        keys = values.keys()
        if "name" not in keys or not values.get("name"):
            raise HTTPException(
                status_code=400,
                detail="Не указано название"
            )
        return values
