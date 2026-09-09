from django.conf import settings
from django.db import models
from doctors.models import Order


class Department(models.Model):
    name = models.CharField(max_length=128, unique=True)
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="departments", blank=True)

    def __str__(self):
        return self.name


class OrderExecution(models.Model):
    """Result produced by a Department after executing a doctor's order."""

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="execution")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="executions")
    result_summary = models.TextField(blank=True)
    # The actual scan/report file is stored via the `documents` app (encrypted).
    executed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Execution of order #{self.order_id} by {self.department.name}"
