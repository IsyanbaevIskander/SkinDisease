from rest_framework import serializers

from core.models import MedicalVerification, SkinCondition
from core.serializers import SkinConditionSerializer


class MedicalVerificationSerializer(serializers.ModelSerializer):
    actual_condition = serializers.PrimaryKeyRelatedField(queryset=SkinCondition.objects.all(), write_only=True)
    actual_condition_detail = SkinConditionSerializer(source='actual_condition', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    doctor_username = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = MedicalVerification
        fields = [
            'id',
            'doctor',
            'doctor_username',
            'doctor_name',
            'result',
            'actual_condition',
            'actual_condition_detail',
        ]
