from sqlalchemy import Column, Integer, Date, DateTime, Text, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from models.model import Base
from utils.utils import calculate_age

'''Модель таблицы повторный приемов в базе данных'''
class RepeatVisitTable(Base):
    __tablename__ = "repeat_visits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    primary_visit_id = Column(Integer, ForeignKey('primary_visits.id'), nullable=False)
    disease_onset_date = Column(Date, nullable=False)
    anamnesis = Column(Text, nullable=False)
    examination = Column(Text, nullable=False)
    prelim_diagnosis = Column(Text, nullable=False)
    confirmed_diagnosis = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    date_visit = Column(DateTime, nullable=False)
    weight = Column(Integer, nullable=True)

    user = relationship("UserTable")  # Связь с врачом
    owner = relationship("OwnerTable")  # Связь с владельцем
    patient = relationship("PatientTable")  # Связь с пациентом
    primary_visit = relationship("PrimaryVisitTable")  # Связь с первичным приемом

    '''Метод для приведения объекта в словарь'''
    def to_dict(self):
        return {
            'id': self.id,
            'primary_visit_id': self.primary_visit_id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'patient_id': self.patient_id,
            'disease_onset_date': self.disease_onset_date.isoformat() if self.disease_onset_date else None,
            'anamnesis': self.anamnesis,
            'examination': self.examination,
            'prelim_diagnosis': self.prelim_diagnosis,
            'confirmed_diagnosis': self.confirmed_diagnosis,
            'result': self.result,
            'date_visit': self.date_visit.isoformat() if self.date_visit else None,
            'weight': float(self.weight) if self.weight else None
        }

    '''Метод для приведения объекта в словарь (используется для журнала посещений)'''
    def to_dict_journal(self):
        return {
            'id': self.id,
            'date_visit': self.date_visit.isoformat() if self.date_visit else None,
            'content': "Повторный прием",
            "doctor_full_name": self.user.last_name + " " + self.user.first_name[0] + ". " + self.user.patronymic[0] + ".",
            "primary_visit_id": self.primary_visit_id
        }

    '''Метод для приведения объекта в словарь (используется в открытии сессии приемов)'''
    def to_dict_visits(self):
        return {
            'id': self.id,
            'primary_visit_id': self.primary_visit_id,
            'user_id': self.user_id,
            'owner_id': self.owner_id,
            'patient_id': self.patient_id,
            'date_visit': self.date_visit.isoformat(),
            'anamnesis': self.anamnesis,
            'examination': self.examination,
            'prelim_diagnosis': self.prelim_diagnosis,
            'confirmed_diagnosis': self.confirmed_diagnosis,
            'result': self.result,
            'weight': float(self.weight) if self.weight else None,
            'disease_onset_date': self.disease_onset_date.isoformat(),
            'breed_name': self.patient.breed.name,
            'animal_name': self.patient.animal_type.name,
            'nickname': self.patient.nickname,
            'age': calculate_age(self.date_visit, self.patient.date_birth),
            'content': "Первичный прием",
            'owner_full_name': self.owner.last_name + " " + self.owner.first_name + " " + self.owner.patronymic,
            'doctor_full_name': self.user.last_name + " " + self.user.first_name + " " + self.user.patronymic,
        }

    '''Метод для приведения объекта в словарь (используется при генерации листа повторного приема)'''
    def to_dict_for_document(self):
        return {
            'id': self.id,
            'doctor': self.user.last_name + " " + self.user.first_name[0] + ". " + self.user.patronymic[0] + ".",
            'owner': self.owner.last_name + " " + self.owner.first_name + ". " + self.owner.patronymic,
            'breed': self.patient.breed.name,
            'nickname': self.patient.nickname,
            'age': calculate_age(self.date_visit, self.patient.date_birth),
            'gender': "Самец" if self.patient.gender == 1 else "Самка" if self.patient.gender == 2 else "Не указано",
            'prelim_diagnosis': self.prelim_diagnosis,
            'confirmed_diagnosis': self.confirmed_diagnosis,
            'disease_onset_date': self.disease_onset_date,
            'anamnesis': self.anamnesis,
            'examination': self.examination,
            'result': self.result,
            'date_visit': self.date_visit.isoformat() if self.date_visit else None,
            'weight': float(self.weight) if self.weight else None
        }