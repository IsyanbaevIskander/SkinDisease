from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token

from core import models


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user: models.User) -> Token:
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)
        user = models.User.objects.filter(id=self.user.pk).first()
        data['role'] = user.role
        data['username'] = user.username
        data['id'] = user.pk
        return data
