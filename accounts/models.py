from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Single user model shared by every stakeholder. The `role` field decides
    what the user can do; `is_approved` is set by the Administrator before
    a Patient or Doctor can actually log in and use the system.
    """

    class Role(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        DOCTOR = "DOCTOR", "Doctor"
        ADMIN = "ADMIN", "Administrator"
        DEPARTMENT = "DEPARTMENT", "Department"
        EMERGENCY = "EMERGENCY", "Emergency Services"

    role = models.CharField(max_length=20, choices=Role.choices)
    is_approved = models.BooleanField(
        default=False,
        help_text="Administrator must approve Patient/Doctor registrations.",
    )
    phone_number = models.CharField(max_length=32, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def needs_approval(self):
        return self.role in (self.Role.PATIENT, self.Role.DOCTOR) and not self.is_approved
