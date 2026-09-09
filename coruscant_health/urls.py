from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from patients.urls import api_urlpatterns as patient_api_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("accounts/", include("accounts.urls")),
    path("patients/", include("patients.urls")),
    path("doctors/", include("doctors.urls")),
    path("departments/", include("departments.urls")),
    path("emergency/", include("emergency.urls")),
    path("documents/", include("documents.urls")),
    path("api/patients/", include((patient_api_urlpatterns, "patients_api"))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
