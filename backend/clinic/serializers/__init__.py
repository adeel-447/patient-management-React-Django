from clinic.serializers.appointment_serializers import (
    AppointmentReadSerializer,
    AppointmentWriteSerializer,
)
from clinic.serializers.clinician_serializers import ClinicianSerializer
from clinic.serializers.patient_serializers import AppointmentSerializer, PatientSerializer

__all__ = [
    "AppointmentReadSerializer",
    "AppointmentSerializer",
    "AppointmentWriteSerializer",
    "ClinicianSerializer",
    "PatientSerializer",
]
