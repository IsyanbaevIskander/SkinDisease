from rest_framework import serializers

from core.models import MedicalVerification


class MedicalVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalVerification
        fields = '__all__'
