from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from .validators import PhoneValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all(
        ), message="Пользователь с таким номером телефона уже существует"), PhoneValidator()]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password_retype = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'password_retype',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password_retype']:
            raise serializers.ValidationError(
                {"password": "Введенные пароли не совпадают"})

        return attrs

    def create(self, validated_data):
        user = get_user_model().objects.create(
            phone=validated_data['phone'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
