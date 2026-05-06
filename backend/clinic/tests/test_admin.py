from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from clinic.models import Clinic

User = get_user_model()


class AdminSiteTests(TestCase):
    def setUp(self):
        clinic = Clinic.objects.create(name="Admin Clinic")
        self.admin = User.objects.create_superuser(
            username="admin", password="admin123", clinic=clinic
        )
        self.client.force_login(self.admin)

    def test_clinic_changelist_loads(self):
        url = reverse("admin:clinic_clinic_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_patient_changelist_loads(self):
        url = reverse("admin:clinic_patient_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_clinician_changelist_loads(self):
        url = reverse("admin:clinic_clinician_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_appointment_changelist_loads(self):
        url = reverse("admin:clinic_appointment_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_changelist_loads(self):
        url = reverse("admin:clinic_user_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
