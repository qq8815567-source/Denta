from pathlib import Path
from datetime import datetime

from dental.infrastructure.file_repository import (
    TextFilePatientRepository,
    TextFileDentistRepository,
    TextFileAppointmentRepository,
)
from dental.services.clinic_service import ClinicService


def _input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "0"


def _parse_dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M")


def main() -> None:
    base = Path.cwd() / "data"
    patients_repo = TextFilePatientRepository(base / "patients.json")
    dentists_repo = TextFileDentistRepository(base / "dentists.json")
    appointments_repo = TextFileAppointmentRepository(base / "appointments.json")
    service = ClinicService(patients_repo, dentists_repo, appointments_repo)

    while True:
        print("1. Register Patient")
        print("2. Add Dentist")
        print("3. Schedule Appointment")
        print("4. View Appointments")
        print("5. Cancel Appointment")
        print("6. View Patients")
        print("7. View Dentists")
        print("0. Exit")
        choice = _input("Choice: ")
        try:
            if choice == "1":
                name = _input("Patient name: ")
                phone = _input("Phone number: ")
                p = service.register_patient(name, phone)
                print(f"Patient ID: {p.id}")
            elif choice == "2":
                name = _input("Dentist name: ")
                spec = _input("Specialty: ")
                d = service.add_dentist(name, spec)
                print(f"Dentist ID: {d.id}")
            elif choice == "3":
                pid = _input("Patient ID: ")
                did = _input("Dentist ID: ")
                start = _parse_dt(_input("Start time (YYYY-MM-DD HH:MM): "))
                end = _parse_dt(_input("End time (YYYY-MM-DD HH:MM): "))
                notes = _input("Notes (optional): ") or None
                a = service.schedule_appointment(pid, did, start, end, notes)
                print(f"Appointment ID: {a.id}")
            elif choice == "4":
                for a in service.list_appointments():
                    print(
                        f"{a.id} Patient:{a.patient_id} Dentist:{a.dentist_id} "
                        f"{a.start_time:%Y-%m-%d %H:%M}-{a.end_time:%Y-%m-%d %H:%M} Status:{a.status}"
                    )
            elif choice == "5":
                aid = _input("Appointment ID: ")
                service.cancel_appointment(aid)
                print("Cancelled")
            elif choice == "6":
                for p in service.list_patients():
                    print(f"{p.id} {p.name} {p.phone}")
            elif choice == "7":
                for d in service.list_dentists():
                    print(f"{d.id} {d.name} {d.specialty}")
            elif choice == "0":
                break
            else:
                print("Invalid choice")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()