from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.mixins import ListModelMixin

from clinic.models import Clinician
from clinic.serializers.clinician_serializers import ClinicianSerializer


class ClinicianViewSet(ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ClinicianSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Clinician.objects.none()
        if not user.clinic_id:
            raise PermissionDenied("Your account is not linked to a clinic.")
        return Clinician.objects.filter(clinic_id=user.clinic_id)
