from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from accounts.models import CustomUser
from accounts.permissions import role_required
from doctors.models import Order
from .models import Department, OrderExecution


@role_required(CustomUser.Role.DEPARTMENT)
def order_queue(request):
    pending_orders = Order.objects.filter(status=Order.Status.PENDING)
    return render(request, "departments/order_queue.html", {"orders": pending_orders})


@role_required(CustomUser.Role.DEPARTMENT)
def execute_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == "POST":
        department, _ = Department.objects.get_or_create(name=request.POST.get("department_name", "General"))
        OrderExecution.objects.create(
            order=order,
            department=department,
            result_summary=request.POST.get("result_summary", ""),
        )
        order.status = Order.Status.EXECUTED
        order.executed_at = timezone.now()
        order.save(update_fields=["status", "executed_at"])
        messages.success(request, "Order marked as executed and results recorded.")
        return redirect("departments:order_queue")
    return render(request, "departments/execute_order.html", {"order": order})
