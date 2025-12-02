from rest_framework import serializers

from core.models import MedicalVerification
from core.serializers import SkinConditionSerializer


class MedicalVerificationSerializer(serializers.ModelSerializer):
    doctor_username = serializers.CharField(source='doctor.username', read_only=True)
    actual_condition = SkinConditionSerializer(read_only=True)

    class Meta:
        model = MedicalVerification
        fields = ['id', 'doctor_username', 'actual_condition', 'doctor', 'result']