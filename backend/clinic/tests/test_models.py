from datetime import date

from django.test import TestCase

from clinic.models import Appointment, Clinic, Clinician, Patient, User


class ClinicModelTests(TestCase):
    def test_str(self):
        clinic = Clinic.objects.create(name="Test Clinic")
        self.assertEqual(str(clinic), "Test Clinic")


class UserModelTests(TestCase):
    def test_str(self):
        clinic = Clinic.objects.create(name="C")
        user = User.objects.create_user(username="testuser", clinic=clinic)
        self.assertEqual(str(user), "testuser")

    def test_user_without_clinic(self):
        user = User.objects.create_user(username="noclinic")
        self.assertIsNone(user.clinic)


class PatientModelTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Patient Clinic")

    def test_str(self):
        patient = Patient.objects.create(
            clinic=self.clinic, first_name="John", last_name="Doe"
        )
        self.assertEqual(str(patient), "John Doe")

    def test_ordering(self):
        Patient.objects.create(
            clinic=self.clinic, first_name="Zack", last_name="Zulu"
        )
        Patient.objects.create(
            clinic=self.clinic, first_name="Adam", last_name="Alpha"
        )
        patients = list(Patient.objects.values_list("last_name", flat=True))
        self.assertEqual(patients, ["Alpha", "Zulu"])

    def test_cascade_delete_clinic_removes_patients(self):
        Patient.objects.create(
            clinic=self.clinic, first_name="Gone", last_name="Soon"
        )
        self.clinic.delete()
        self.assertEqual(Patient.objects.count(), 0)


class ClinicianModelTests(TestCase):
    def test_str(self):
        clinic = Clinic.objects.create(name="C")
        clinician = Clinician.objects.create(
            clinic=clinic, first_name="Dr", last_name="Smith"
        )
        self.assertEqual(str(clinician), "Dr Smith")

    def test_ordering(self):
        clinic = Clinic.objects.create(name="C")
        Clinician.objects.create(clinic=clinic, first_name="Zed", last_name="Zulu")
        Clinician.objects.create(clinic=clinic, first_name="Ann", last_name="Alpha")
        clinicians = list(Clinician.objects.values_list("last_name", flat=True))
        self.assertEqual(clinicians, ["Alpha", "Zulu"])


class AppointmentModelTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(name="Appt Clinic")
        self.patient = Patient.objects.create(
            clinic=self.clinic, first_name="Pat", last_name="Ient"
        )

    def test_str(self):
        appt = Appointment.objects.create(
            patient=self.patient, scheduled_at="2025-06-01T10:00:00Z"
        )
        self.assertIn("Pat Ient", str(appt))

    def test_many_clinicians(self):
        c1 = Clinician.objects.create(
            clinic=self.clinic, first_name="Dr", last_name="One"
        )
        c2 = Clinician.objects.create(
            clinic=self.clinic, first_name="Dr", last_name="Two"
        )
        appt = Appointment.objects.create(
            patient=self.patient, scheduled_at="2025-07-01T09:00:00Z"
        )
        appt.clinicians.set([c1, c2])
        self.assertEqual(appt.clinicians.count(), 2)

    def test_cascade_delete_patient_removes_appointments(self):
        Appointment.objects.create(
            patient=self.patient, scheduled_at="2025-08-01T11:00:00Z"
        )
        self.patient.delete()
        self.assertEqual(Appointment.objects.count(), 0)

    def test_ordering_by_scheduled_at_desc(self):
        Appointment.objects.create(
            patient=self.patient, scheduled_at="2025-01-01T10:00:00Z"
        )
        Appointment.objects.create(
            patient=self.patient, scheduled_at="2025-12-01T10:00:00Z"
        )
        appts = list(
            Appointment.objects.values_list("scheduled_at", flat=True)
        )
        self.assertGreater(appts[0], appts[1])
