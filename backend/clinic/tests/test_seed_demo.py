from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase

from clinic.models import Appointment, Clinic, Clinician, Patient

User = get_user_model()


class SeedDemoCommandTests(TestCase):
    def test_seed_creates_demo_data(self):
        call_command("seed_demo")
        self.assertTrue(User.objects.filter(username="demo").exists())
        self.assertTrue(Clinic.objects.filter(name="Demo Community Clinic").exists())
        self.assertGreaterEqual(Patient.objects.count(), 2)
        self.assertGreaterEqual(Clinician.objects.count(), 2)
        self.assertGreaterEqual(Appointment.objects.count(), 2)

    def test_seed_is_idempotent(self):
        call_command("seed_demo")
        call_command("seed_demo")
        self.assertEqual(User.objects.filter(username="demo").count(), 1)
        self.assertEqual(Clinic.objects.filter(name="Demo Community Clinic").count(), 1)

    def test_seed_user_can_authenticate(self):
        call_command("seed_demo")
        user = User.objects.get(username="demo")
        self.assertTrue(user.check_password("demo1234"))
        self.assertTrue(user.is_staff)
        self.assertIsNotNone(user.clinic)

    def test_seed_appointments_have_clinicians(self):
        call_command("seed_demo")
        for appt in Appointment.objects.all():
            self.assertGreater(appt.clinicians.count(), 0)

    def test_seed_custom_password(self):
        call_command("seed_demo", "--password=custom123")
        user = User.objects.get(username="demo")
        self.assertTrue(user.check_password("custom123"))
