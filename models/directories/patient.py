import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base
from utils.utils import calculate_age


class PatientTable(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(255))
    animal_type_id = Column(Integer, ForeignKey('animal_types.id'), nullable=False)
    breed_id = Column(Integer, ForeignKey('breeds.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.id'))
    date_birth = Column(Date, nullable=False)
    gender = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    # Определяем отношения с другими таблицами
    animal_type = relationship("AnimalTypeTable")
    breed = relationship("BreedTable")
    owner = relationship("OwnerTable")

    def to_dict_page(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "animal_type_id": self.animal_type_id,
            "breed_id": self.breed_id,
            "owner_id": self.owner_id,
            "date_birth": self.date_birth,
            "gender": self.gender,
            "created_at": self.created_at,
            "animal_type_name": self.animal_type.name,
            "breed_name": self.breed.name,
        }

    def to_dict_fast_search(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "animal_type_name": self.animal_type.name,
            "breed_name": self.breed.name,
            "date_birth": self.date_birth,
            "owner_fullname": self.owner.name + " " + self.owner.last_name + " " + self.owner.patronymic,
        }

    def to_dict(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "animal_type_id": self.animal_type_id,
            "breed_id": self.breed_id,
            "owner_id": self.owner_id,
            "date_birth": self.date_birth,
            "gender": self.gender,
            "created_at": self.created_at,
        }

    def to_dict_info(self):
        return {
            "id": self.id,
            "nickname": self.nickname,

            "animal_type_name": self.animal_type.name,
            "breed_name": self.breed.name,
            "color": "в скором времени добавим поле",
            "castrated": "в скором времени добавим поле",

            "age": calculate_age(datetime.datetime.now(), self.date_birth),
            "date_birth": self.date_birth.isoformat() if self.date_birth else None,
            "gender": self.gender,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
