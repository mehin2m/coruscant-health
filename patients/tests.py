from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from .models import PatientProfile, HealthReading


class HealthReadingApiTests(TestCase):
    def setUp(self):
        self.patient_user = CustomUser.objects.create_user(
            username="p1", password="pw12345", role=CustomUser.Role.PATIENT, is_approved=True
        )
        self.client.force_login(self.patient_user)

    def test_patient_can_upload_reading(self):
        response = self.client.post(reverse("patients_api:readings-api"), {
            "reading_type": "HEART_RATE", "value": 72.5, "unit": "bpm", "recorded_at": "2026-01-01T10:00:00Z",
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(HealthReading.objects.count(), 1)

    def test_other_role_cannot_upload_reading(self):
        doctor = CustomUser.objects.create_user(
            username="d1", password="pw12345", role=CustomUser.Role.DOCTOR, is_approved=True
        )
        self.client.force_login(doctor)
        response = self.client.post(reverse("patients_api:readings-api"), {
            "reading_type": "HEART_RATE", "value": 72.5, "recorded_at": "2026-01-01T10:00:00Z",
        })
        self.assertEqual(response.status_code, 403)

    def test_patient_dashboard_lists_own_readings(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.patient_user)
        HealthReading.objects.create(
            patient=profile, reading_type="HEART_RATE", value=80, recorded_at="2026-01-01T10:00:00Z"
        )
        response = self.client.get(reverse("patients:dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "80.0")
