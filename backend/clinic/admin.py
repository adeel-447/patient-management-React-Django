from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from clinic.models import Appointment, Clinic, Clinician, Patient, User


@admin.register(Clinic)
class ClinicAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = ("username", "email", "clinic", "is_staff")
    list_filter = ("is_staff", "clinic")
    fieldsets = DjangoUserAdmin.fieldsets + (("Clinic", {"fields": ("clinic",)}),)  # type: ignore[assignment]
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("Clinic", {"fields": ("clinic",)}),)  # type: ignore[assignment]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "clinic", "email", "phone")
    list_filter = ("clinic",)


@admin.register(Clinician)
class ClinicianAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "clinic")
    list_filter = ("clinic",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "scheduled_at")
    list_filter = ("patient__clinic",)
    filter_horizontal = ("clinicians",)
