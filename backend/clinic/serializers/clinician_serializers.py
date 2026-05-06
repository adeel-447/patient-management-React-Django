from rest_framework import serializers

from clinic.models import Clinician


class ClinicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinician
        fields = ("id", "first_name", "last_name")
        read_only_fields = ("id",)
