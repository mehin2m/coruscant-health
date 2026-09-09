from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from accounts.models import CustomUser


@login_required
def home(request):
    user = request.user
    if user.needs_approval:
        return redirect("accounts:pending_approval")
    routes = {
        CustomUser.Role.PATIENT: "patients:dashboard",
        CustomUser.Role.DOCTOR: "doctors:dashboard",
        CustomUser.Role.DEPARTMENT: "departments:order_queue",
        CustomUser.Role.EMERGENCY: "emergency:quick_intake",
        CustomUser.Role.ADMIN: "accounts:approve_users",
    }
    return redirect(routes.get(user.role, "accounts:login"))
