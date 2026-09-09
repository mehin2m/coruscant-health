from django import forms
from accounts.models import CustomUser


class QuickPatientIntakeForm(forms.Form):
    """Minimal fields, optimized for speed during an emergency."""

    full_name = forms.CharField(max_length=150)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date"}))
    condition_notes = forms.CharField(widget=forms.Textarea, required=False)
