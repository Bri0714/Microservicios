# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError
import re

UserModel = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password', 'password2')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        # Validación de contraseña
        if len(value) < 8:
            raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.findall(r'\d', value):
            raise ValidationError("La contraseña debe contener al menos un número.")
        if not re.findall(r'[A-Z]', value):
            raise ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.findall(r'[!@#$%^&*(),.?\":{}|<>]', value):
            raise ValidationError("La contraseña debe contener al menos un carácter especial.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise ValidationError({"password2": "Las contraseñas no coinciden."})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = UserModel.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise ValidationError('Usuario no encontrado o credenciales incorrectas.')
        return data

class UserSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'new_password', 'confirm_password')

    def validate_email(self, value):
        user = self.instance
        if UserModel.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def validate_username(self, value):
        user = self.instance
        if UserModel.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if new_password or confirm_password:
            if new_password != confirm_password:
                raise ValidationError({"confirm_password": "Las contraseñas no coinciden."})
            if len(new_password) < 8:
                raise ValidationError({"new_password": "La contraseña debe tener al menos 8 caracteres."})
            # Agrega más validaciones si es necesario

        return data

    def update(self, instance, validated_data):
        validated_data.pop('confirm_password', None)
        new_password = validated_data.pop('new_password', None)

        email = validated_data.get('email')
        username = validated_data.get('username')

        if email is not None:
            instance.email = email
        if username is not None:
            instance.username = username

        if new_password:
            instance.set_password(new_password)
        instance.save()
        return instance