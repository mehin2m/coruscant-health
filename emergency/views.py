import uuid
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import CustomUser
from accounts.permissions import role_required
from patients.models import PatientProfile
from doctors.models import Report
from .forms import QuickPatientIntakeForm


@role_required(CustomUser.Role.EMERGENCY)
def quick_intake(request):
    if request.method == "POST":
        form = QuickPatientIntakeForm(request.POST)
        if form.is_valid():
            # Auto-generate a login so the patient record exists immediately;
            # Administrator can reconcile/merge the account later.
            username = f"er-{uuid.uuid4().hex[:8]}"
            user = CustomUser.objects.create_user(
                username=username,
                password=uuid.uuid4().hex,
                role=CustomUser.Role.PATIENT,
                is_approved=True,  # emergency intake skips the normal approval wait
                first_name=form.cleaned_data["full_name"],
            )
            profile = PatientProfile.objects.create(
                user=user, date_of_birth=form.cleaned_data.get("date_of_birth")
            )
            if form.cleaned_data.get("condition_notes"):
                messages.info(request, form.cleaned_data["condition_notes"])
            messages.success(request, f"Patient registered. Temporary ID: {username}")
            return redirect("emergency:quick_intake")
    else:
        form = QuickPatientIntakeForm()
    return render(request, "emergency/quick_intake.html", {"form": form})
