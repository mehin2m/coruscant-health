from django.test import TestCase
from django.urls import reverse
from .models import CustomUser


class CustomUserTests(TestCase):
    def test_patient_needs_approval_by_default(self):
        user = CustomUser.objects.create_user(username="pat1", password="pw12345", role=CustomUser.Role.PATIENT)
        self.assertTrue(user.needs_approval)

    def test_admin_never_needs_approval(self):
        admin = CustomUser.objects.create_user(username="adm1", password="pw12345", role=CustomUser.Role.ADMIN)
        self.assertFalse(admin.needs_approval)

    def test_registration_creates_unapproved_user(self):
        response = self.client.post(reverse("accounts:register"), {
            "username": "newdoc", "email": "d@example.com", "phone_number": "",
            "role": CustomUser.Role.DOCTOR, "password1": "StrongPass123!", "password2": "StrongPass123!",
        })
        self.assertEqual(response.status_code, 302)
        user = CustomUser.objects.get(username="newdoc")
        self.assertFalse(user.is_approved)

    def test_unapproved_user_cannot_reach_role_view(self):
        user = CustomUser.objects.create_user(username="pat2", password="pw12345", role=CustomUser.Role.PATIENT)
        self.client.force_login(user)
        response = self.client.get(reverse("patients:dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_approve_pending_user(self):
        admin = CustomUser.objects.create_user(username="adm2", password="pw12345", role=CustomUser.Role.ADMIN)
        pending = CustomUser.objects.create_user(username="pat3", password="pw12345", role=CustomUser.Role.PATIENT)
        self.client.force_login(admin)
        response = self.client.post(reverse("accounts:approve_users"), {"user_id": pending.id})
        self.assertEqual(response.status_code, 302)
        pending.refresh_from_db()
        self.assertTrue(pending.is_approved)
