from sqlalchemy import Column, Integer, String, Date, DateTime
from models.model import Base

class OwnerTable(Base):
    __tablename__ = "owners"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    patronymic = Column(String(255), nullable=False)
    address = Column(String(255))
    date_birth = Column(Date)
    gender = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)

    def to_dict_for_document(self):
        return {
            'id': self.id,
            'owner': self.last_name + " " + self.first_name + " " + self.patronymic,
            'address': self.last_name + " " + self.first_name + " " + self.patronymic,
        }