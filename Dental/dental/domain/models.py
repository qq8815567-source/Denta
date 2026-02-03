from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Patient:
    id: str
    name: str
    phone: str


@dataclass(frozen=True)
class Dentist:
    id: str
    name: str
    specialty: str


@dataclass(frozen=True)
class Appointment:
    id: str
    patient_id: str
    dentist_id: str
    start_time: datetime
    end_time: datetime
    status: str = "scheduled"
    notes: Optional[str] = None