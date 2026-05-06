from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from clinic.models import Appointment, Clinic, Clinician, Patient

User = get_user_model()

SAMPLE_PATIENTS = [
    {"first_name": "Sam", "last_name": "Rivera", "date_of_birth": date(1985, 3, 14), "email": "sam@example.com", "phone": "555-0100"},
    {"first_name": "Jordan", "last_name": "Nguyen", "date_of_birth": date(1990, 7, 22), "email": "jordan@example.com", "phone": "555-0101"},
    {"first_name": "Olivia", "last_name": "Martinez", "date_of_birth": date(1978, 11, 5), "email": "olivia.m@example.com", "phone": "555-0102"},
    {"first_name": "Liam", "last_name": "Johnson", "date_of_birth": date(1995, 1, 30), "email": "liam.j@example.com", "phone": "555-0103"},
    {"first_name": "Emma", "last_name": "Williams", "date_of_birth": date(1988, 6, 18), "email": "emma.w@example.com", "phone": "555-0104"},
    {"first_name": "Noah", "last_name": "Brown", "date_of_birth": date(1972, 9, 2), "email": "noah.b@example.com", "phone": "555-0105"},
    {"first_name": "Ava", "last_name": "Jones", "date_of_birth": date(2000, 4, 12), "email": "ava.jones@example.com", "phone": "555-0106"},
    {"first_name": "William", "last_name": "Garcia", "date_of_birth": date(1965, 12, 25), "email": "will.g@example.com", "phone": "555-0107"},
    {"first_name": "Sophia", "last_name": "Miller", "date_of_birth": date(1993, 8, 7), "email": "sophia.m@example.com", "phone": "555-0108"},
    {"first_name": "James", "last_name": "Davis", "date_of_birth": date(1982, 2, 14), "email": "james.d@example.com", "phone": "555-0109"},
    {"first_name": "Isabella", "last_name": "Rodriguez", "date_of_birth": date(1997, 5, 20), "email": "isabella.r@example.com", "phone": "555-0110"},
    {"first_name": "Benjamin", "last_name": "Wilson", "date_of_birth": date(1970, 10, 31), "email": "ben.w@example.com", "phone": "555-0111"},
    {"first_name": "Mia", "last_name": "Anderson", "date_of_birth": date(1991, 3, 8), "email": "mia.a@example.com", "phone": "555-0112"},
    {"first_name": "Lucas", "last_name": "Thomas", "date_of_birth": date(1986, 7, 15), "email": "lucas.t@example.com", "phone": "555-0113"},
    {"first_name": "Charlotte", "last_name": "Taylor", "date_of_birth": date(1999, 11, 28), "email": "charlotte.t@example.com", "phone": "555-0114"},
    {"first_name": "Henry", "last_name": "Moore", "date_of_birth": date(1975, 4, 3), "email": "henry.m@example.com", "phone": "555-0115"},
    {"first_name": "Amelia", "last_name": "Jackson", "date_of_birth": date(1989, 9, 19), "email": "amelia.j@example.com", "phone": "555-0116"},
    {"first_name": "Alexander", "last_name": "Martin", "date_of_birth": date(1968, 1, 11), "email": "alex.m@example.com", "phone": "555-0117"},
    {"first_name": "Harper", "last_name": "Lee", "date_of_birth": date(2001, 6, 6), "email": "harper.l@example.com", "phone": "555-0118"},
    {"first_name": "Daniel", "last_name": "Thompson", "date_of_birth": date(1984, 12, 9), "email": "daniel.t@example.com", "phone": "555-0119"},
    {"first_name": "Evelyn", "last_name": "White", "date_of_birth": date(1996, 8, 23), "email": "evelyn.w@example.com", "phone": "555-0120"},
    {"first_name": "Michael", "last_name": "Harris", "date_of_birth": date(1973, 2, 17), "email": "michael.h@example.com", "phone": "555-0121"},
    {"first_name": "Abigail", "last_name": "Clark", "date_of_birth": date(1994, 10, 4), "email": "abigail.c@example.com", "phone": "555-0122"},
    {"first_name": "Ethan", "last_name": "Lewis", "date_of_birth": date(1980, 5, 27), "email": "ethan.l@example.com", "phone": "555-0123"},
    {"first_name": "Emily", "last_name": "Robinson", "date_of_birth": date(1987, 7, 1), "email": "emily.r@example.com", "phone": "555-0124"},
]


class Command(BaseCommand):
    help = "Create a demo clinic, staff user, clinicians, patients, and appointments."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default="demo1234",
            help="Password for the demo staff user (default: demo1234)",
        )

    def handle(self, *args, **options):
        password = options["password"]

        clinic, _ = Clinic.objects.get_or_create(name="Demo Community Clinic")

        user, created = User.objects.get_or_create(
            username="demo",
            defaults={
                "email": "demo@example.com",
                "clinic": clinic,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user 'demo' with password '{password}'."))
        else:
            user.clinic = clinic
            user.is_staff = True
            user.is_superuser = True
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.WARNING(f"Updated user 'demo' with password '{password}'."))

        dr_smith, _ = Clinician.objects.get_or_create(
            clinic=clinic, first_name="Jane", last_name="Smith",
        )
        dr_lee, _ = Clinician.objects.get_or_create(
            clinic=clinic, first_name="Alex", last_name="Lee",
        )
        dr_patel, _ = Clinician.objects.get_or_create(
            clinic=clinic, first_name="Raj", last_name="Patel",
        )

        patients = []
        for data in SAMPLE_PATIENTS:
            patient, _ = Patient.objects.get_or_create(
                clinic=clinic,
                first_name=data["first_name"],
                last_name=data["last_name"],
                defaults={
                    "date_of_birth": data["date_of_birth"],
                    "email": data["email"],
                    "phone": data["phone"],
                },
            )
            patients.append(patient)

        self.stdout.write(f"  {len(patients)} patients ready.")

        clinicians = [dr_smith, dr_lee, dr_patel]
        when = timezone.now().replace(microsecond=0)
        appt_count = 0
        for i, patient in enumerate(patients[:10]):
            appt, was_created = Appointment.objects.get_or_create(
                patient=patient,
                scheduled_at=when + timezone.timedelta(hours=(i + 1) * 12),
                defaults={"notes": f"Appointment #{i + 1}"},
            )
            if was_created or appt.clinicians.count() == 0:
                assigned = [clinicians[i % len(clinicians)]]
                if i % 3 == 0:
                    assigned.append(clinicians[(i + 1) % len(clinicians)])
                appt.clinicians.set(assigned)
                appt_count += 1

        self.stdout.write(f"  {appt_count} appointments created/updated.")
        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
