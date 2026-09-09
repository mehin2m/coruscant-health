from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="accounts:login"), name="logout"),
    path("pending/", views.pending_approval, name="pending_approval"),
    path("approve/", views.approve_users, name="approve_users"),
]
