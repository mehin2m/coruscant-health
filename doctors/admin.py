from django.contrib import admin
from .models import DoctorProfile, Report, Order

admin.site.register(DoctorProfile)
admin.site.register(Report)
admin.site.register(Order)
