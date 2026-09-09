from django.urls import path
from . import views

app_name = "doctors"

urlpatterns = [
    path("dashboard/", views.doctor_dashboard, name="dashboard"),
    path("patient/<int:patient_id>/", views.patient_detail, name="patient_detail"),
]
