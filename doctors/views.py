import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import CustomUser
from accounts.permissions import role_required
from patients.models import PatientProfile
from .models import DoctorProfile, Report, Order


@role_required(CustomUser.Role.DOCTOR)
def doctor_dashboard(request):
    profile, _ = DoctorProfile.objects.get_or_create(user=request.user)
    patients = PatientProfile.objects.filter(reports__doctor=profile).distinct()
    return render(request, "doctors/dashboard.html", {"patients": patients})


@role_required(CustomUser.Role.DOCTOR)
def patient_detail(request, patient_id):
    profile, _ = DoctorProfile.objects.get_or_create(user=request.user)
    patient = get_object_or_404(PatientProfile, pk=patient_id)
    readings = patient.readings.all()[:100]

    if request.method == "POST":
        if "write_report" in request.POST:
            Report.objects.create(
                doctor=profile,
                patient=patient,
                content=request.POST.get("content", ""),
                condition_trend=request.POST.get("condition_trend", "STABLE"),
            )
            messages.success(request, "Report saved.")
        elif "new_order" in request.POST:
            Order.objects.create(
                doctor=profile,
                patient=patient,
                order_type=request.POST.get("order_type"),
                notes=request.POST.get("notes", ""),
            )
            messages.success(request, "Order submitted to department.")
        return redirect("doctors:patient_detail", patient_id=patient.id)

    reports = patient.reports.all()
    orders = patient.orders.all()
    # Readings serialized simply for the trend chart (Chart.js consumes this).
    chart_data = json.dumps(
        [{"x": r.recorded_at.isoformat(), "y": r.value, "type": r.reading_type} for r in readings]
    )
    return render(
        request,
        "doctors/patient_detail.html",
        {
            "patient": patient,
            "readings": readings,
            "reports": reports,
            "orders": orders,
            "chart_data": chart_data,
        },
    )
