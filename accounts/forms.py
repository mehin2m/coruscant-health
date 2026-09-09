from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class PatientDoctorRegistrationForm(UserCreationForm):
    """Used by both Patient and Doctor self-registration pages."""

    role = forms.ChoiceField(choices=[
        (CustomUser.Role.PATIENT, "Patient"),
        (CustomUser.Role.DOCTOR, "Doctor"),
    ])

    class Meta:
        model = CustomUser
        fields = ["username", "email", "phone_number", "role", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_approved = False
        if commit:
            user.save()
        return user
