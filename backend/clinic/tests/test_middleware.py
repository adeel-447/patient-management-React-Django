from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from clinic.models import Clinic

User = get_user_model()


class RequestIdMiddlewareTests(APITestCase):
    def setUp(self):
        clinic = Clinic.objects.create(name="Main Clinic")
        self.user = User.objects.create_user(
            username="request-id-user",
            password="testpass123",
            clinic=clinic,
        )
        self.client.force_authenticate(self.user)

    def test_response_contains_request_id_header(self):
        response = self.client.get(reverse("patient-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("X-Request-ID", response.headers)
        self.assertTrue(response.headers["X-Request-ID"])
