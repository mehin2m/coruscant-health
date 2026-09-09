from django.conf import settings
from django.db import models
from patients.models import PatientProfile


class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    specialty = models.CharField(max_length=128, blank=True)

    def __str__(self):
        return f"Dr. {self.user.username}"


class Report(models.Model):
    """A doctor's prescription / recommendation written for a patient."""

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="reports")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="reports")
    content = models.TextField()
    condition_trend = models.CharField(
        max_length=16,
        choices=[("IMPROVING", "Improving"), ("STABLE", "Stable"), ("WORSENING", "Worsening")],
        default="STABLE",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Report for {self.patient.user.username} by {self.doctor.user.username}"


class Order(models.Model):
    """An order for a service, e.g. CT scan, PET scan, raised by a doctor."""

    class OrderType(models.TextChoices):
        CT_SCAN = "CT_SCAN", "CT Scan"
        PET_SCAN = "PET_SCAN", "PET Scan"
        BLOOD_TEST = "BLOOD_TEST", "Blood Test"
        MRI = "MRI", "MRI"
        OTHER = "OTHER", "Other"

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        EXECUTED = "EXECUTED", "Executed"
        CANCELLED = "CANCELLED", "Cancelled"

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name="orders")
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="orders")
    order_type = models.CharField(max_length=32, choices=OrderType.choices)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    executed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.order_type} for {self.patient.user.username} ({self.status})"
