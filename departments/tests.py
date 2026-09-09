from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser
from patients.models import PatientProfile
from doctors.models import DoctorProfile, Order
from .models import Department, OrderExecution


class DepartmentExecutionTests(TestCase):
    def setUp(self):
        self.dept_user = CustomUser.objects.create_user(
            username="dept1", password="pw12345", role=CustomUser.Role.DEPARTMENT, is_approved=True
        )
        doctor_user = CustomUser.objects.create_user(
            username="doc2", password="pw12345", role=CustomUser.Role.DOCTOR, is_approved=True
        )
        patient_user = CustomUser.objects.create_user(
            username="pat2", password="pw12345", role=CustomUser.Role.PATIENT, is_approved=True
        )
        doctor_profile = DoctorProfile.objects.create(user=doctor_user)
        patient_profile = PatientProfile.objects.create(user=patient_user)
        self.order = Order.objects.create(doctor=doctor_profile, patient=patient_profile, order_type="CT_SCAN")
        self.client.force_login(self.dept_user)

    def test_executing_order_updates_status(self):
        response = self.client.post(
            reverse("departments:execute_order", args=[self.order.id]),
            {"department_name": "Radiology", "result_summary": "Clear scan"},
        )
        self.assertEqual(response.status_code, 302)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.EXECUTED)
        self.assertEqual(OrderExecution.objects.count(), 1)
