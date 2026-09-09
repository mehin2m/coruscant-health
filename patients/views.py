from rest_framework import generics, permissions
from django.shortcuts import render
from accounts.models import CustomUser
from accounts.permissions import role_required
from .models import PatientProfile, HealthReading
from .serializers import HealthReadingSerializer


class IsOwnerPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == CustomUser.Role.PATIENT
            and not request.user.needs_approval
        )


class HealthReadingUploadView(generics.ListCreateAPIView):
    """
    Device data upload endpoint.
    POST /api/patients/readings/  -> upload a new reading
    GET  /api/patients/readings/  -> list this patient's readings
    """

    serializer_class = HealthReadingSerializer
    permission_classes = [IsOwnerPatient]

    def get_queryset(self):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        return profile.readings.all()

    def perform_create(self, serializer):
        profile, _ = PatientProfile.objects.get_or_create(user=self.request.user)
        serializer.save(patient=profile)


@role_required(CustomUser.Role.PATIENT)
def patient_dashboard(request):
    profile, _ = PatientProfile.objects.get_or_create(user=request.user)
    readings = profile.readings.all()[:50]
    from doctors.models import Report

    reports = Report.objects.filter(patient=profile).order_by("-created_at")
    return render(
        request, "patients/dashboard.html", {"readings": readings, "reports": reports}
    )
