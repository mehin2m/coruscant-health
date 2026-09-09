from django.conf import settings
from django.db import models


class PatientProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="patient_profile"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    device_id = models.CharField(max_length=64, blank=True, help_text="ID of the wearable device.")

    def __str__(self):
        return f"Patient: {self.user.username}"


class HealthReading(models.Model):
    """A single reading uploaded by the patient's device."""

    class ReadingType(models.TextChoices):
        HEART_RATE = "HEART_RATE", "Heart Rate"
        BLOOD_PRESSURE = "BLOOD_PRESSURE", "Blood Pressure"
        BLOOD_OXYGEN = "BLOOD_OXYGEN", "Blood Oxygen"
        TEMPERATURE = "TEMPERATURE", "Temperature"
        GLUCOSE = "GLUCOSE", "Glucose"
        OTHER = "OTHER", "Other"

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, related_name="readings")
    reading_type = models.CharField(max_length=32, choices=ReadingType.choices)
    value = models.FloatField()
    unit = models.CharField(max_length=16, blank=True)
    recorded_at = models.DateTimeField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self):
        return f"{self.patient.user.username} - {self.reading_type}: {self.value}"
