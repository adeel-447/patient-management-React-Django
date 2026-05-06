from django.contrib.auth.models import AbstractUser
from django.db import models

from clinic.models.clinic import Clinic


class User(AbstractUser):
    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="staff",
    )

    def __str__(self) -> str:
        return self.username
