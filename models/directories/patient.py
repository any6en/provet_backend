import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from models.model import Base
from utils.utils import calculate_age

'''Модель таблицы пациентов в базе данных'''
class PatientTable(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    animal_type_id = Column(Integer, ForeignKey('animal_types.id'), nullable=False)
    breed_id = Column(Integer, ForeignKey('breeds.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    nickname = Column(String(25), nullable=False)
    color = Column(String(50))
    is_castrated = Column(Boolean, nullable=False)

    date_birth = Column(Date, nullable=False)
    gender = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    animal_type = relationship("AnimalTypeTable") # Связь с типом
    breed = relationship("BreedTable") # Связь с породой
    owner = relationship("OwnerTable") # Связь с владельцом

    '''Метод для приведения объекта в словарь'''
    def to_dict(self):
        return {
            "id": self.id,
            "animal_type_id": self.animal_type_id,
            "breed_id": self.breed_id,
            "owner_id": self.owner_id,
            "nickname": self.nickname,
            "color": self.color,
            "is_castrated": self.is_castrated,
            "date_birth": self.date_birth.isoformat(),
            "gender": self.gender,
            "created_at": self.created_at.isoformat(),
        }

    '''Метод для приведения объекта в словарь (используется для справочника)'''
    def to_dict_page(self):
        return {
            "id": self.id,
            "animal_type_id": self.animal_type_id,
            "breed_id": self.breed_id,
            "owner_id": self.owner_id,
            "nickname": self.nickname,
            "color": self.color,
            "is_castrated": self.is_castrated,
            "date_birth": self.date_birth.isoformat(),
            "gender": self.gender,
            "created_at": self.created_at.isoformat(),
            "animal_type_name": self.animal_type.name,
            "breed_name": self.breed.name,
        }

    '''Метод для приведения объекта в словарь (используется для быстрого поиска)'''
    def to_dict_fast_search(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "animal_type_name": self.animal_type.name,
            "breed_name": self.breed.name,
            "date_birth": self.date_birth,
            "owner_fullname": self.owner.name + " " + self.owner.last_name + " " + self.owner.patronymic,
        }



    '''Метод для приведения объекта в словарь (используется для получения доп. информации в свойствах)'''
    def to_dict_info(self):
        return {
            "id": self.id,
            "nickname": self.nickname,

            "animal_type_name": self.animal_type.name,
            "breed_name": self.breed.name,
            "color": self.color,
            "is_castrated": self.is_castrated,

            "age": calculate_age(datetime.datetime.now(), self.date_birth),
            "date_birth": self.date_birth.isoformat() if self.date_birth else None,
            "gender": self.gender,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
