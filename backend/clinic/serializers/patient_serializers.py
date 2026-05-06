from rest_framework import serializers

from clinic.models import Appointment, Patient


class AppointmentSerializer(serializers.ModelSerializer):
    clinician_names = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = ("id", "scheduled_at", "notes", "clinician_names")

    def get_clinician_names(self, obj: Appointment) -> list[str]:
        return [str(c) for c in obj.clinicians.all()]


class PatientSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = (
            "id",
            "first_name",
            "last_name",
            "date_of_birth",
            "email",
            "phone",
            "created_at",
            "updated_at",
            "appointments",
        )
        read_only_fields = ("id", "created_at", "updated_at", "appointments")

    def validate_first_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters.")
        return value

    def validate_last_name(self, value: str) -> str:
        value = value.strip()
        if len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters.")
        return value

    def validate_phone(self, value: str) -> str:
        value = value.strip()
        if value and len(value) < 7:
            raise serializers.ValidationError("Phone number looks too short.")
        return value

    def validate_email(self, value: str) -> str:
        value = value.strip().lower()
        if not value:
            return value
        validator = serializers.EmailField()
        validator.run_validation(value)
        return value
