from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base


class VaccinationActTable(Base):
    __tablename__ = "vaccination_acts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Ссылка на врача
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)  # Ссылка на владельца
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)  # Ссылка на пациента
    vaccine = Column(String(255), nullable=False)  # Вакцина
    vaccination_date = Column(Date, nullable=False)  # Дата вакцинации
    revaccination_date = Column(Date, nullable=True)  # Дата ревакцинации
    weight = Column(Integer, nullable=True)

    # Опциональные связи (если нужно)
    user = relationship("UserTable")  # Предполагая, что у вас есть модель User
    owner = relationship("OwnerTable")  # Предполагая, что у вас есть модель Owner
    patient = relationship("PatientTable")  # Предполагая, что у вас есть модель Patient

    def to_dict_journal(self):
        return {
            'id': self.id,
            'date_visit': self.vaccination_date.isoformat() if self.vaccination_date else None,
            'content': "Акт вакцинации",
            "doctor_full_name": self.user.last_name + " " + self.user.first_name[0] + ". " + self.user.patronymic[0] + ".",
            "primary_visit_id": None
        }