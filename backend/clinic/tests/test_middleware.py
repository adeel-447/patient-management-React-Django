import json
from unittest.mock import patch

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

    def test_request_id_is_uuid_format(self):
        response = self.client.get(reverse("patient-list"))
        request_id = response.headers["X-Request-ID"]
        parts = request_id.split("-")
        self.assertEqual(len(parts), 5)

    def test_propagates_incoming_request_id(self):
        custom_id = "my-custom-request-id-12345"
        response = self.client.get(
            reverse("patient-list"), HTTP_X_REQUEST_ID=custom_id
        )
        self.assertEqual(response.headers["X-Request-ID"], custom_id)

    @patch("clinic.middleware.audit_logger")
    def test_audit_log_emitted(self, mock_logger):
        self.client.get(reverse("patient-list"))
        mock_logger.info.assert_called_once()
        log_payload = json.loads(mock_logger.info.call_args[0][0])
        self.assertEqual(log_payload["event"], "http_request")
        self.assertEqual(log_payload["method"], "GET")
        self.assertIn("duration_ms", log_payload)
        self.assertEqual(log_payload["user_id"], self.user.id)

    @patch("clinic.middleware.audit_logger")
    def test_audit_log_for_unauthenticated_user(self, mock_logger):
        self.client.force_authenticate(None)
        self.client.get(reverse("patient-list"))
        mock_logger.info.assert_called_once()
        log_payload = json.loads(mock_logger.info.call_args[0][0])
        self.assertIsNone(log_payload["user_id"])

    @patch("clinic.middleware.audit_logger")
    def test_audit_log_contains_path_and_status(self, mock_logger):
        self.client.get(reverse("health"))
        mock_logger.info.assert_called_once()
        log_payload = json.loads(mock_logger.info.call_args[0][0])
        self.assertEqual(log_payload["path"], "/api/health/")
        self.assertEqual(log_payload["status_code"], 200)

    @patch("clinic.middleware.audit_logger")
    def test_audit_log_captures_x_forwarded_for(self, mock_logger):
        self.client.get(
            reverse("patient-list"),
            HTTP_X_FORWARDED_FOR="203.0.113.50, 70.41.3.18",
        )
        log_payload = json.loads(mock_logger.info.call_args[0][0])
        self.assertEqual(log_payload["client_ip"], "203.0.113.50")
