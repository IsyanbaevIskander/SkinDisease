from rest_framework import serializers

from core.models import DiagnosisRequest


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosisRequest
        fields = '__all__'
