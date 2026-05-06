from django.db import models

from clinic.models.clinician import Clinician
from clinic.models.patient import Patient


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="appointments")
    scheduled_at = models.DateTimeField()
    notes = models.TextField(blank=True)
    clinicians = models.ManyToManyField(Clinician, related_name="appointments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-scheduled_at"]

    def __str__(self) -> str:
        return f"{self.patient} @ {self.scheduled_at}"
