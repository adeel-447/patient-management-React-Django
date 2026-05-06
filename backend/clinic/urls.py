from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from clinic.views import AppointmentViewSet, ClinicianViewSet, PatientViewSet, health

router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("appointments", AppointmentViewSet, basename="appointment")
router.register("clinicians", ClinicianViewSet, basename="clinician")

urlpatterns = [
    path("health/", health, name="health"),
    path("auth/login/", TokenObtainPairView.as_view(), name="auth_login"),
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
