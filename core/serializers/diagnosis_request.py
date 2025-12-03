from rest_framework import serializers

from core.models import DiagnosisRequest
from core.serializers.diagnosis_result import DiagnosisResultSerializer


class DiagnosisRequestSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    result = DiagnosisResultSerializer(read_only=True)

    class Meta:
        model = DiagnosisRequest
        fields = ['id', 'image', 'created_at', 'user', 'user_name', 'result']
