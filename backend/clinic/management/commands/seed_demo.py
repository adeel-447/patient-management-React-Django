from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from clinic.models import Appointment, Clinic, Clinician, Patient

User = get_user_model()


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
            },
        )
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"Created user 'demo' with password '{password}'."))
        else:
            user.clinic = clinic
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.WARNING(f"Updated user 'demo' with password '{password}'."))

        dr_smith, _ = Clinician.objects.get_or_create(
            clinic=clinic,
            first_name="Jane",
            last_name="Smith",
        )
        dr_lee, _ = Clinician.objects.get_or_create(
            clinic=clinic,
            first_name="Alex",
            last_name="Lee",
        )

        p1, _ = Patient.objects.get_or_create(
            clinic=clinic,
            first_name="Sam",
            last_name="Rivera",
            defaults={
                "email": "sam@example.com",
                "phone": "555-0100",
            },
        )
        p2, _ = Patient.objects.get_or_create(
            clinic=clinic,
            first_name="Jordan",
            last_name="Nguyen",
            defaults={"phone": "555-0101"},
        )

        when = timezone.now().replace(microsecond=0)
        for patient, offset_hours in ((p1, 24), (p2, 48)):
            appt, created = Appointment.objects.get_or_create(
                patient=patient,
                scheduled_at=when + timezone.timedelta(hours=offset_hours),
                defaults={"notes": "Follow-up visit"},
            )
            if created or appt.clinicians.count() == 0:
                appt.clinicians.set([dr_smith, dr_lee])

        self.stdout.write(self.style.SUCCESS("Demo data is ready."))
