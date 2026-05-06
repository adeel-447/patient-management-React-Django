from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter

from clinic.models import Patient
from clinic.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["first_name", "last_name", "email", "phone"]
    ordering_fields = ["last_name", "first_name", "created_at", "updated_at"]
    ordering = ["last_name", "first_name"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Patient.objects.none()
        if not user.clinic_id:
            raise PermissionDenied("Your account is not linked to a clinic.")
        return Patient.objects.filter(clinic_id=user.clinic_id).prefetch_related(
            "appointments__clinicians"
        )

    def perform_create(self, serializer):
        user = self.request.user
        if not user.clinic_id:
            raise PermissionDenied("Your account is not linked to a clinic.")
        serializer.save(clinic_id=user.clinic_id)

    def perform_update(self, serializer):
        user = self.request.user
        if not user.clinic_id:
            raise PermissionDenied("Your account is not linked to a clinic.")
        if serializer.instance.clinic_id != user.clinic_id:
            raise PermissionDenied("You cannot modify patients from another clinic.")
        serializer.save()

    def perform_destroy(self, instance: Patient):
        user = self.request.user
        if not user.clinic_id:
            raise PermissionDenied("Your account is not linked to a clinic.")
        if instance.clinic_id != user.clinic_id:
            raise PermissionDenied("You cannot delete patients from another clinic.")
        instance.delete()
