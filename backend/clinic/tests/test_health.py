from django.urls import reverse
from rest_framework.test import APITestCase


class HealthEndpointTests(APITestCase):
    def test_health_returns_200(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_health_no_auth_required(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
