from rest_framework import serializers

from clinic.models import Appointment, Clinician, Patient


class AppointmentReadSerializer(serializers.ModelSerializer):
    clinician_names = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ("id", "patient", "scheduled_at", "notes", "clinicians", "clinician_names", "created_at")
        read_only_fields = ("id", "created_at", "clinician_names")

    def get_clinician_names(self, obj: Appointment) -> list[str]:
        return [str(c) for c in obj.clinicians.all()]


class AppointmentWriteSerializer(serializers.ModelSerializer):
    clinicians = serializers.PrimaryKeyRelatedField(
        queryset=Clinician.objects.all(), many=True
    )

    class Meta:
        model = Appointment
        fields = ("id", "patient", "scheduled_at", "notes", "clinicians", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_patient(self, value: Patient) -> Patient:
        request = self.context.get("request")
        if request and value.clinic_id != request.user.clinic_id:
            raise serializers.ValidationError("Patient does not belong to your clinic.")
        return value

    def validate_clinicians(self, value: list[Clinician]) -> list[Clinician]:
        request = self.context.get("request")
        if not request:
            return value
        for clinician in value:
            if clinician.clinic_id != request.user.clinic_id:
                raise serializers.ValidationError(
                    f"Clinician '{clinician}' does not belong to your clinic."
                )
        return value
