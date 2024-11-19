from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from models.model import Base

'''Модель таблицы актов вакцинации в базе данных'''
class VaccinationActTable(Base):
    __tablename__ = "vaccination_acts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    vaccine = Column(String(255), nullable=False)
    vaccination_date = Column(Date, nullable=False)
    revaccination_date = Column(Date, nullable=True)
    weight = Column(Integer, nullable=True)

    # Опциональные связи (если нужно)
    user = relationship("UserTable")  # Связь с врачом
    owner = relationship("OwnerTable")  # Связь с владельцем
    patient = relationship("PatientTable")  # Связь с пациентом

    '''Метод для приведения объекта в словарь (используется для журнала посещений)'''
    def to_dict_journal(self):
        return {
            'id': self.id,
            'date_visit': self.vaccination_date.isoformat() if self.vaccination_date else None,
            'content': "Акт вакцинации",
            "doctor_full_name": self.user.last_name + " " + self.user.first_name[0] + ". " + self.user.patronymic[0] + ".",
            "primary_visit_id": None
        }