from rest_framework import serializers
from core.models import DiagnosisRequest

class DiagnosisRequestSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    result = serializers.SerializerMethodField()
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = DiagnosisRequest
        fields = ['id', 'user', 'user_username', 'image', 'created_at', 'result']

    def get_result(self, obj):
        if hasattr(obj, 'result') and obj.result:
            from core.serializers.diagnosis_result import DiagnosisResultSerializer
            return DiagnosisResultSerializer(obj.result).data
        return None
