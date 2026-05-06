from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

from clinic.models import Appointment
from clinic.serializers.appointment_serializers import (
    AppointmentReadSerializer,
    AppointmentWriteSerializer,
)


class AppointmentViewSet(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return AppointmentWriteSerializer
        return AppointmentReadSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Appointment.objects.none()
        if not user.clinic_id:
            raise PermissionDenied("Your account is not linked to a clinic.")
        return Appointment.objects.filter(
            patient__clinic_id=user.clinic_id
        ).prefetch_related("clinicians")

    def perform_destroy(self, instance: Appointment):
        user = self.request.user
        if instance.patient.clinic_id != user.clinic_id:
            raise PermissionDenied("You cannot delete appointments from another clinic.")
        instance.delete()
