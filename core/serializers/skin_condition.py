from rest_framework import serializers

from core.models import SkinCondition


class SkinConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinCondition
        fields = ['id', 'name', 'code', 'description']