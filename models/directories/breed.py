from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base


class BreedTable(Base):
    __tablename__ = "breeds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    animal_type_id = Column(Integer, ForeignKey('animal_types.id'))

    animal_type = relationship("AnimalTypeTable", back_populates="breeds")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "animal_type_id": self.animal_type_id,
        }

    def to_dict_full(self):
        return {
            "id": self.id,
            "name": self.name,
            "animal_type_id": self.animal_type_id,
            "animal_type_name": self.animal_type.name if self.animal_type else None
        }
