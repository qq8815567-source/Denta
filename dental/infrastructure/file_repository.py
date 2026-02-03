from pathlib import Path
import json
from typing import List, Optional
from datetime import datetime

from dental.domain.models import Patient, Dentist, Appointment
from dental.domain.repositories import (
    PatientRepository,
    DentistRepository,
    AppointmentRepository,
)


def _ensure_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("[]", encoding="utf-8")


def _dt_to_str(dt: datetime) -> str:
    return dt.isoformat()


def _dt_from_str(s: str) -> datetime:
    return datetime.fromisoformat(s)


class TextFilePatientRepository(PatientRepository):
    def __init__(self, path: Path) -> None:
        self.path = path
        _ensure_file(self.path)

    def add(self, patient: Patient) -> None:
        items = self.list()
        items.append(patient)
        self._save(items)

    def get_by_id(self, patient_id: str) -> Optional[Patient]:
        for p in self.list():
            if p.id == patient_id:
                return p
        return None

    def list(self) -> List[Patient]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Patient(**item) for item in raw]

    def update(self, patient: Patient) -> None:
        items = [p for p in self.list() if p.id != patient.id]
        items.append(patient)
        self._save(items)

    def delete(self, patient_id: str) -> None:
        items = [p for p in self.list() if p.id != patient_id]
        self._save(items)

    def _save(self, patients: List[Patient]) -> None:
        data = [vars(p) for p in patients]
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class TextFileDentistRepository(DentistRepository):
    def __init__(self, path: Path) -> None:
        self.path = path
        _ensure_file(self.path)

    def add(self, dentist: Dentist) -> None:
        items = self.list()
        items.append(dentist)
        self._save(items)

    def get_by_id(self, dentist_id: str) -> Optional[Dentist]:
        for d in self.list():
            if d.id == dentist_id:
                return d
        return None

    def list(self) -> List[Dentist]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [Dentist(**item) for item in raw]

    def update(self, dentist: Dentist) -> None:
        items = [d for d in self.list() if d.id != dentist.id]
        items.append(dentist)
        self._save(items)

    def delete(self, dentist_id: str) -> None:
        items = [d for d in self.list() if d.id != dentist_id]
        self._save(items)

    def _save(self, dentists: List[Dentist]) -> None:
        data = [vars(d) for d in dentists]
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


class TextFileAppointmentRepository(AppointmentRepository):
    def __init__(self, path: Path) -> None:
        self.path = path
        _ensure_file(self.path)

    def add(self, appointment: Appointment) -> None:
        items = self.list_all()
        items.append(appointment)
        self._save(items)

    def get_by_id(self, appointment_id: str) -> Optional[Appointment]:
        for a in self.list_all():
            if a.id == appointment_id:
                return a
        return None

    def list_all(self) -> List[Appointment]:
        raw = json.loads(self.path.read_text(encoding="utf-8"))
        return [self._from_dict(item) for item in raw]

    def list_by_dentist_between(self, dentist_id: str, start: datetime, end: datetime) -> List[Appointment]:
        return [
            a
            for a in self.list_all()
            if a.dentist_id == dentist_id and not (a.end_time <= start or a.start_time >= end)
        ]

    def list_by_patient(self, patient_id: str) -> List[Appointment]:
        return [a for a in self.list_all() if a.patient_id == patient_id]

    def update(self, appointment: Appointment) -> None:
        items = [a for a in self.list_all() if a.id != appointment.id]
        items.append(appointment)
        self._save(items)

    def delete(self, appointment_id: str) -> None:
        items = [a for a in self.list_all() if a.id != appointment_id]
        self._save(items)

    def _save(self, appointments: List[Appointment]) -> None:
        data = [self._to_dict(a) for a in appointments]
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def _to_dict(self, a: Appointment) -> dict:
        return {
            "id": a.id,
            "patient_id": a.patient_id,
            "dentist_id": a.dentist_id,
            "start_time": _dt_to_str(a.start_time),
            "end_time": _dt_to_str(a.end_time),
            "status": a.status,
            "notes": a.notes,
        }

    def _from_dict(self, d: dict) -> Appointment:
        return Appointment(
            id=d["id"],
            patient_id=d["patient_id"],
            dentist_id=d["dentist_id"],
            start_time=_dt_from_str(d["start_time"]),
            end_time=_dt_from_str(d["end_time"]),
            status=d.get("status", "scheduled"),
            notes=d.get("notes"),
        )