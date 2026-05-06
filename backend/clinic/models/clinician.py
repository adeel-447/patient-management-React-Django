from django.db import models

from clinic.models.clinic import Clinic


class Clinician(models.Model):
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name="clinicians")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
