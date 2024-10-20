from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.model import Base

class AnimalTypeTable(Base):
    __tablename__ = "animal_types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    # Отношение один-ко-многим
    breeds = relationship("BreedTable", back_populates="animal_type")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }


