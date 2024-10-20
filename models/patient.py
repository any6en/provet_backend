from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base

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
