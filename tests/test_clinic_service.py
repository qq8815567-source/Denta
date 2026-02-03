import unittest
from pathlib import Path
from datetime import datetime, timedelta
import tempfile

from dental.infrastructure.file_repository import (
    TextFilePatientRepository,
    TextFileDentistRepository,
    TextFileAppointmentRepository,
)
from dental.services.clinic_service import ClinicService


class ClinicServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.p_repo = TextFilePatientRepository(base / "patients.json")
        self.d_repo = TextFileDentistRepository(base / "dentists.json")
        self.a_repo = TextFileAppointmentRepository(base / "appointments.json")
        self.svc = ClinicService(self.p_repo, self.d_repo, self.a_repo)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_register_and_add_dentist(self):
        p = self.svc.register_patient("John Doe", "13800000000")
        d = self.svc.add_dentist("Jane Smith", "Orthodontics")
        self.assertEqual(len(self.svc.list_patients()), 1)
        self.assertEqual(len(self.svc.list_dentists()), 1)
        self.assertEqual(self.svc.list_patients()[0].id, p.id)
        self.assertEqual(self.svc.list_dentists()[0].id, d.id)

    def test_schedule_no_conflict(self):
        p = self.svc.register_patient("Alice", "1")
        d = self.svc.add_dentist("Bob", "Endodontics")
        start = datetime.now().replace(microsecond=0)
        end = start + timedelta(minutes=30)
        a = self.svc.schedule_appointment(p.id, d.id, start, end)
        self.assertEqual(a.status, "scheduled")
        self.assertEqual(len(self.svc.list_appointments()), 1)

    def test_schedule_conflict_raises(self):
        p = self.svc.register_patient("Alice", "1")
        d = self.svc.add_dentist("Bob", "Endodontics")
        start = datetime.now().replace(microsecond=0)
        end = start + timedelta(minutes=30)
        self.svc.schedule_appointment(p.id, d.id, start, end)
        with self.assertRaises(ValueError):
            self.svc.schedule_appointment(p.id, d.id, start + timedelta(minutes=10), end + timedelta(minutes=10))

    def test_cancel_appointment(self):
        p = self.svc.register_patient("Alice", "1")
        d = self.svc.add_dentist("Bob", "Endodontics")
        start = datetime(2026, 1, 1, 9, 0)
        end = datetime(2026, 1, 1, 9, 30)
        a = self.svc.schedule_appointment(p.id, d.id, start, end)
        self.svc.cancel_appointment(a.id)
        a2 = self.a_repo.get_by_id(a.id)
        self.assertEqual(a2.status, "cancelled")

    def test_invalid_time_range(self):
        p = self.svc.register_patient("Alice", "1")
        d = self.svc.add_dentist("Bob", "Endodontics")
        start = datetime(2026, 1, 1, 10, 0)
        end = datetime(2026, 1, 1, 9, 0)
        with self.assertRaises(ValueError):
            self.svc.schedule_appointment(p.id, d.id, start, end)


if __name__ == "__main__":
    unittest.main()