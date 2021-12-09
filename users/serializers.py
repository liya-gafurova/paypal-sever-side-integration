from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import TokenSerializer, LoginSerializer


class LoginSerializerCustom(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True, allow_blank=False)


class TokenSerializerCustom(TokenSerializer):
    pass


class RegisterSerializerCustom(RegisterSerializer):
    pass

