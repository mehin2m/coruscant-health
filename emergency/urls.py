from django.urls import path
from . import views

app_name = "emergency"

urlpatterns = [
    path("intake/", views.quick_intake, name="quick_intake"),
]
