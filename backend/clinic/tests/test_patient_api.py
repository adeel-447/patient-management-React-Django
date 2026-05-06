from datetime import date

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clinic.models import Appointment, Clinic, Clinician, Patient

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

    # ─── LIST ────────────────────────────────────────────────────────────

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

    def test_list_unauthenticated_returns_401(self):
        self.client.force_authenticate(None)
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_nested_appointments_with_clinicians(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a,
            first_name="Dana",
            last_name="Doe",
        )
        clinician = Clinician.objects.create(
            clinic=self.clinic_a, first_name="Dr", last_name="Who"
        )
        appt = Appointment.objects.create(
            patient=patient, scheduled_at="2025-06-01T10:00:00Z", notes="Checkup"
        )
        appt.clinicians.add(clinician)

        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        result = response.data["results"][0]
        self.assertEqual(len(result["appointments"]), 1)
        self.assertEqual(result["appointments"][0]["notes"], "Checkup")
        self.assertIn("Dr Who", result["appointments"][0]["clinician_names"])

    def test_list_search_by_first_name(self):
        Patient.objects.create(
            clinic=self.clinic_a, first_name="Charlie", last_name="One"
        )
        Patient.objects.create(
            clinic=self.clinic_a, first_name="Dave", last_name="Two"
        )
        response = self.client.get(reverse("patient-list"), {"search": "Charlie"})
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["first_name"], "Charlie")

    def test_list_search_by_email(self):
        Patient.objects.create(
            clinic=self.clinic_a,
            first_name="Eve",
            last_name="Three",
            email="eve@test.com",
        )
        Patient.objects.create(
            clinic=self.clinic_a, first_name="Frank", last_name="Four"
        )
        response = self.client.get(reverse("patient-list"), {"search": "eve@test"})
        self.assertEqual(response.data["count"], 1)

    def test_list_ordering(self):
        Patient.objects.create(
            clinic=self.clinic_a, first_name="Zara", last_name="Zulu"
        )
        Patient.objects.create(
            clinic=self.clinic_a, first_name="Adam", last_name="Alpha"
        )
        response = self.client.get(
            reverse("patient-list"), {"ordering": "last_name"}
        )
        names = [r["last_name"] for r in response.data["results"]]
        self.assertEqual(names, ["Alpha", "Zulu"])

    def test_list_user_without_clinic_gets_403(self):
        no_clinic_user = User.objects.create_user(
            username="orphan", password="testpass123", clinic=None
        )
        self.client.force_authenticate(no_clinic_user)
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ─── RETRIEVE ────────────────────────────────────────────────────────

    def test_retrieve_own_clinic_patient(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a,
            first_name="Greg",
            last_name="Good",
            email="greg@test.com",
        )
        response = self.client.get(reverse("patient-detail", args=[patient.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "greg@test.com")

    def test_retrieve_other_clinic_patient_returns_404(self):
        patient = Patient.objects.create(
            clinic=self.clinic_b, first_name="Hidden", last_name="Patient"
        )
        response = self.client.get(reverse("patient-detail", args=[patient.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ─── CREATE ──────────────────────────────────────────────────────────

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

    def test_create_patient_without_optional_fields(self):
        payload = {"first_name": "Min", "last_name": "Fields"}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "")
        self.assertEqual(response.data["phone"], "")
        self.assertIsNone(response.data["date_of_birth"])

    def test_create_patient_user_without_clinic_gets_403(self):
        no_clinic_user = User.objects.create_user(
            username="no-clinic", password="testpass123", clinic=None
        )
        self.client.force_authenticate(no_clinic_user)
        payload = {"first_name": "Nope", "last_name": "NoClinic"}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ─── UPDATE ──────────────────────────────────────────────────────────

    def test_update_own_clinic_patient(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a, first_name="Old", last_name="Name"
        )
        response = self.client.patch(
            reverse("patient-detail", args=[patient.id]),
            {"first_name": "New"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.first_name, "New")

    def test_full_update_patient(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a,
            first_name="Full",
            last_name="Update",
            email="old@test.com",
        )
        payload = {
            "first_name": "Fully",
            "last_name": "Updated",
            "email": "new@test.com",
            "phone": "5559999999",
            "date_of_birth": "2000-01-01",
        }
        response = self.client.put(
            reverse("patient-detail", args=[patient.id]), payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient.refresh_from_db()
        self.assertEqual(patient.email, "new@test.com")

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

    def test_update_user_without_clinic_gets_403(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a, first_name="Pat", last_name="Ient"
        )
        no_clinic_user = User.objects.create_user(
            username="updater-no-clinic", password="testpass123", clinic=None
        )
        self.client.force_authenticate(no_clinic_user)
        response = self.client.patch(
            reverse("patient-detail", args=[patient.id]),
            {"first_name": "Attempt"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ─── DELETE ──────────────────────────────────────────────────────────

    def test_delete_own_clinic_patient(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a, first_name="Del", last_name="Eted"
        )
        response = self.client.delete(reverse("patient-detail", args=[patient.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Patient.objects.filter(id=patient.id).exists())

    def test_cross_clinic_delete_is_forbidden(self):
        patient = Patient.objects.create(
            clinic=self.clinic_b, first_name="Cant", last_name="Touch"
        )
        response = self.client.delete(reverse("patient-detail", args=[patient.id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_user_without_clinic_gets_403(self):
        patient = Patient.objects.create(
            clinic=self.clinic_a, first_name="Target", last_name="Delete"
        )
        no_clinic_user = User.objects.create_user(
            username="deleter-no-clinic", password="testpass123", clinic=None
        )
        self.client.force_authenticate(no_clinic_user)
        response = self.client.delete(
            reverse("patient-detail", args=[patient.id])
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ─── VALIDATION ──────────────────────────────────────────────────────

    def test_name_validation_too_short(self):
        payload = {"first_name": "A", "last_name": "B"}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)

    def test_name_validation_strips_whitespace(self):
        payload = {"first_name": "  Valid  ", "last_name": "  Name  "}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["first_name"], "Valid")
        self.assertEqual(response.data["last_name"], "Name")

    def test_phone_validation_too_short(self):
        payload = {"first_name": "Phone", "last_name": "Test", "phone": "123"}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", response.data)

    def test_phone_validation_empty_is_allowed(self):
        payload = {"first_name": "Phone", "last_name": "Empty", "phone": ""}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_email_validation_invalid_format(self):
        payload = {
            "first_name": "Email",
            "last_name": "Invalid",
            "email": "not-an-email",
        }
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_email_validation_normalized_to_lowercase(self):
        payload = {
            "first_name": "Email",
            "last_name": "Lower",
            "email": "Test@Example.COM",
        }
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_email_empty_is_allowed(self):
        payload = {"first_name": "No", "last_name": "Email", "email": ""}
        response = self.client.post(reverse("patient-list"), payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PatientApiAuthTests(APITestCase):
    """Test JWT login endpoint."""

    def setUp(self):
        clinic = Clinic.objects.create(name="Auth Clinic")
        self.user = User.objects.create_user(
            username="authuser", password="secure123", clinic=clinic
        )

    def test_login_returns_tokens(self):
        response = self.client.post(
            reverse("auth_login"),
            {"username": "authuser", "password": "secure123"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_wrong_password_returns_401(self):
        response = self.client.post(
            reverse("auth_login"),
            {"username": "authuser", "password": "wrong"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_refresh(self):
        login_response = self.client.post(
            reverse("auth_login"),
            {"username": "authuser", "password": "secure123"},
            format="json",
        )
        refresh_token = login_response.data["refresh"]
        response = self.client.post(
            reverse("token_refresh"),
            {"refresh": refresh_token},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
