from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from patients.models import PatientProfile


class QuickIntakeTests(TestCase):
    def setUp(self):
        self.er_user = CustomUser.objects.create_user(
            username="er1", password="pw12345", role=CustomUser.Role.EMERGENCY, is_approved=True
        )
        self.client.force_login(self.er_user)

    def test_quick_intake_creates_approved_patient(self):
        response = self.client.post(reverse("emergency:quick_intake"), {
            "full_name": "Jane Doe", "condition_notes": "Unconscious on arrival",
        })
        self.assertEqual(response.status_code, 302)
        patient = PatientProfile.objects.first()
        self.assertIsNotNone(patient)
        self.assertTrue(patient.user.is_approved)
        self.assertEqual(patient.intake_notes, "Unconscious on arrival")
