from django.urls import path
from . import views

app_name = "departments"

urlpatterns = [
    path("orders/", views.order_queue, name="order_queue"),
    path("orders/<int:order_id>/execute/", views.execute_order, name="execute_order"),
]
