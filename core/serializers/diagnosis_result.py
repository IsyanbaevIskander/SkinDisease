from rest_framework import serializers

from core.models import DiagnosisResult
from core.serializers.medical_verification import MedicalVerificationSerializer
from core.serializers.skin_condition import SkinConditionSerializer


class DiagnosisResultSerializer(serializers.ModelSerializer):
    condition = SkinConditionSerializer(read_only=True)
    verification = MedicalVerificationSerializer(read_only=True)

    class Meta:
        model = DiagnosisResult
        fields = ['id', 'condition', 'confidence', 'verification']
