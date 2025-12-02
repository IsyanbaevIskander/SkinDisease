from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'username', 'role', 'password')

    def create(self, validated_data: dict) -> User:
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        if new_password := validated_data.get('password'):
            validated_data['password'] = make_password(new_password)
        return super().update(instance, validated_data)
