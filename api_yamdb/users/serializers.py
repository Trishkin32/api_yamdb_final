from rest_framework import serializers

from users.models import User
from users.validators import ValidateUsername


class UserSerializer(ValidateUsername, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):

        read_only_fields = ('role',)


class RegistrationSerializer(ValidateUsername, serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )


class TokenSerializer(ValidateUsername, serializers.Serializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    confirmation_code = serializers.CharField(
        required=True,
    )
