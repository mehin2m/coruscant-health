from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [
    path("dashboard/", views.patient_dashboard, name="dashboard"),
]

api_urlpatterns = [
    path("readings/", views.HealthReadingUploadView.as_view(), name="readings-api"),
]
