from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import PatientDoctorRegistrationForm
from .models import CustomUser
from .permissions import role_required


def register(request):
    if request.method == "POST":
        form = PatientDoctorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                "Registration submitted. An Administrator must approve your "
                "account before you can log in.",
            )
            return redirect("accounts:login")
    else:
        form = PatientDoctorRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def pending_approval(request):
    return render(request, "accounts/pending_approval.html")


@role_required(CustomUser.Role.ADMIN)
def approve_users(request):
    pending_users = CustomUser.objects.filter(
        role__in=[CustomUser.Role.PATIENT, CustomUser.Role.DOCTOR],
        is_approved=False,
    )
    if request.method == "POST":
        user = get_object_or_404(CustomUser, pk=request.POST.get("user_id"))
        user.is_approved = True
        user.save(update_fields=["is_approved"])
        messages.success(request, f"{user.username} approved.")
        return redirect("accounts:approve_users")
    return render(request, "accounts/approve_users.html", {"pending_users": pending_users})
