from rest_framework import serializers
from .models import HealthReading


class HealthReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthReading
        fields = ["id", "reading_type", "value", "unit", "recorded_at", "uploaded_at"]
        read_only_fields = ["id", "uploaded_at"]
