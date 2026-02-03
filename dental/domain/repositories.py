from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from .models import Patient, Dentist, Appointment


class PatientRepository(ABC):
    @abstractmethod
    def add(self, patient: Patient) -> None:
        ...

    @abstractmethod
    def get_by_id(self, patient_id: str) -> Optional[Patient]:
        ...

    @abstractmethod
    def list(self) -> List[Patient]:
        ...

    @abstractmethod
    def update(self, patient: Patient) -> None:
        ...

    @abstractmethod
    def delete(self, patient_id: str) -> None:
        ...


class DentistRepository(ABC):
    @abstractmethod
    def add(self, dentist: Dentist) -> None:
        ...

    @abstractmethod
    def get_by_id(self, dentist_id: str) -> Optional[Dentist]:
        ...

    @abstractmethod
    def list(self) -> List[Dentist]:
        ...

    @abstractmethod
    def update(self, dentist: Dentist) -> None:
        ...

    @abstractmethod
    def delete(self, dentist_id: str) -> None:
        ...


class AppointmentRepository(ABC):
    @abstractmethod
    def add(self, appointment: Appointment) -> None:
        ...

    @abstractmethod
    def get_by_id(self, appointment_id: str) -> Optional[Appointment]:
        ...

    @abstractmethod
    def list_all(self) -> List[Appointment]:
        ...

    @abstractmethod
    def list_by_dentist_between(self, dentist_id: str, start: datetime, end: datetime) -> List[Appointment]:
        ...

    @abstractmethod
    def list_by_patient(self, patient_id: str) -> List[Appointment]:
        ...

    @abstractmethod
    def update(self, appointment: Appointment) -> None:
        ...

    @abstractmethod
    def delete(self, appointment_id: str) -> None:
        ...