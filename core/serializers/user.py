from rest_framework import serializers

from core.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'username', 'role', 'password')
