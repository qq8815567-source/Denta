from typing import List, Optional
from uuid import uuid4
from datetime import datetime

from dental.domain.models import Patient, Dentist, Appointment
from dental.domain.repositories import (
    PatientRepository,
    DentistRepository,
    AppointmentRepository,
)


class ClinicService:
    def __init__(
        self,
        patients: PatientRepository,
        dentists: DentistRepository,
        appointments: AppointmentRepository,
    ) -> None:
        self.patients = patients
        self.dentists = dentists
        self.appointments = appointments

    def register_patient(self, name: str, phone: str) -> Patient:
        pid = str(uuid4())
        p = Patient(id=pid, name=name, phone=phone)
        self.patients.add(p)
        return p

    def add_dentist(self, name: str, specialty: str) -> Dentist:
        did = str(uuid4())
        d = Dentist(id=did, name=name, specialty=specialty)
        self.dentists.add(d)
        return d

    def schedule_appointment(
        self,
        patient_id: str,
        dentist_id: str,
        start_time: datetime,
        end_time: datetime,
        notes: Optional[str] = None,
    ) -> Appointment:
        if start_time >= end_time:
            raise ValueError("invalid time range")

        patient = self.patients.get_by_id(patient_id)
        if not patient:
            raise ValueError("patient not found")

        dentist = self.dentists.get_by_id(dentist_id)
        if not dentist:
            raise ValueError("dentist not found")

        conflicts = self.appointments.list_by_dentist_between(
            dentist_id, start_time, end_time
        )
        conflicts = [a for a in conflicts if a.status == "scheduled"]
        if conflicts:
            raise ValueError("appointment conflicts")

        aid = str(uuid4())
        a = Appointment(
            id=aid,
            patient_id=patient_id,
            dentist_id=dentist_id,
            start_time=start_time,
            end_time=end_time,
            status="scheduled",
            notes=notes,
        )
        self.appointments.add(a)
        return a

    def cancel_appointment(self, appointment_id: str) -> None:
        a = self.appointments.get_by_id(appointment_id)
        if not a:
            raise ValueError("appointment not found")
        a = Appointment(
            id=a.id,
            patient_id=a.patient_id,
            dentist_id=a.dentist_id,
            start_time=a.start_time,
            end_time=a.end_time,
            status="cancelled",
            notes=a.notes,
        )
        self.appointments.update(a)

    def list_patients(self) -> List[Patient]:
        return self.patients.list()

    def list_dentists(self) -> List[Dentist]:
        return self.dentists.list()

    def list_appointments(self) -> List[Appointment]:
        return self.appointments.list_all()

    def list_appointments_for_patient(self, patient_id: str) -> List[Appointment]:
        return self.appointments.list_by_patient(patient_id)