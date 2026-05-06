from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clinic.models import Clinic, Patient

User = get_user_model()


class PatientApiTests(APITestCase):
    def setUp(self):
        self.clinic_a = Clinic.objects.create(name="Clinic A")
        self.clinic_b = Clinic.objects.create(name="Clinic B")
        self.user = User.objects.create_user(
            username="alice",
            password="testpass123",
            clinic=self.clinic_a,
        )
        self.other_user = User.objects.create_user(
            username="bob",
            password="testpass123",
            clinic=self.clinic_b,
        )
        self.client.force_authenticate(self.user)

    def test_list_only_returns_same_clinic(self):
        Patient.objects.create(
            clinic=self.clinic_a,
            first_name="Anne",
            last_name="Able",
            date_of_birth=date(1990, 1, 1),
        )
        Patient.objects.create(
            clinic=self.clinic_b,
            first_name="Ben",
            last_name="Baker",
            date_of_birth=date(1992, 2, 2),
        )

        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["last_name"], "Able")

    def test_create_patient_attaches_user_clinic(self):
        payload = {
            "first_name": "Jane",
            "last_name": "Doe",
            "date_of_birth": "1988-04-01",
            "email": "jane@example.com",
            "phone": "5551234567",
        }
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patient = Patient.objects.get(id=response.data["id"])
        self.assertEqual(patient.clinic_id, self.clinic_a.id)

    def test_cross_clinic_update_is_forbidden(self):
        patient = Patient.objects.create(
            clinic=self.clinic_b,
            first_name="Chris",
            last_name="Cross",
        )
        response = self.client.patch(
            reverse("patient-detail", args=[patient.id]),
            {"first_name": "Changed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_name_validation(self):
        payload = {
            "first_name": "A",
            "last_name": "B",
        }
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
