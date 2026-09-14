from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from patients.models import PatientProfile
from .models import DoctorProfile, Report, Order


class DoctorWorkflowTests(TestCase):
    def setUp(self):
        self.doctor_user = CustomUser.objects.create_user(
            username="doc1", password="pw12345", role=CustomUser.Role.DOCTOR, is_approved=True
        )
        self.patient_user = CustomUser.objects.create_user(
            username="pat1", password="pw12345", role=CustomUser.Role.PATIENT, is_approved=True
        )
        self.patient_profile = PatientProfile.objects.create(user=self.patient_user)
        self.client.force_login(self.doctor_user)

    def test_doctor_can_write_report(self):
        response = self.client.post(
            reverse("doctors:patient_detail", args=[self.patient_profile.id]),
            {"write_report": "1", "content": "Rest and hydrate", "condition_trend": "IMPROVING"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 1)
        self.assertEqual(Report.objects.first().condition_trend, "IMPROVING")

    def test_doctor_can_submit_order(self):
        response = self.client.post(
            reverse("doctors:patient_detail", args=[self.patient_profile.id]),
            {"new_order": "1", "order_type": "CT_SCAN", "notes": "Check lungs"},
        )
        self.assertEqual(response.status_code, 302)
        order = Order.objects.first()
        self.assertEqual(order.order_type, "CT_SCAN")
        self.assertEqual(order.status, Order.Status.PENDING)

class DoctorPatientApprovalPermissionTests(TestCase):
    """Ensures a doctor cannot view or act on a patient whose registration
    has not yet been approved by the Administrator."""

    def setUp(self):
        self.doctor_user = CustomUser.objects.create_user(
            username="doc2", password="pw12345", role=CustomUser.Role.DOCTOR, is_approved=True
        )
        self.approved_patient_user = CustomUser.objects.create_user(
            username="pat_approved", password="pw12345",
            role=CustomUser.Role.PATIENT, is_approved=True,
        )
        self.unapproved_patient_user = CustomUser.objects.create_user(
            username="pat_unapproved", password="pw12345",
            role=CustomUser.Role.PATIENT, is_approved=False,
        )
        self.approved_profile = PatientProfile.objects.create(user=self.approved_patient_user)
        self.unapproved_profile = PatientProfile.objects.create(user=self.unapproved_patient_user)
        self.client.force_login(self.doctor_user)

    def test_doctor_can_view_approved_patient(self):
        response = self.client.get(
            reverse("doctors:patient_detail", args=[self.approved_profile.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_doctor_cannot_view_unapproved_patient(self):
        response = self.client.get(
            reverse("doctors:patient_detail", args=[self.unapproved_profile.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("doctors:dashboard"))

    def test_doctor_cannot_write_report_for_unapproved_patient(self):
        response = self.client.post(
            reverse("doctors:patient_detail", args=[self.unapproved_profile.id]),
            {"write_report": "1", "content": "Should not be saved", "condition_trend": "STABLE"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Report.objects.count(), 0)
