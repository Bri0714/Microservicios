# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework.exceptions import ValidationError
import re
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

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
    
# serializers para confiramcion y olvido de contraseaña 
#class PasswordResetRequestSerializer(serializers.Serializer):
#    email = serializers.EmailField()
#
#    def validate_email(self, value):
#        try:
#            user = UserModel.objects.get(email=value)
#        except UserModel.DoesNotExist:
#            raise serializers.ValidationError("No se encontró un usuario con ese correo electrónico.")
#        return value
#
#    def save(self):
#        request = self.context.get('request')
#        email = self.validated_data['email']
#        user = UserModel.objects.get(email=email)
#        token_generator = PasswordResetTokenGenerator()
#        token = token_generator.make_token(user)
#        uid = urlsafe_base64_encode(force_bytes(user.pk))
#        
#        # Construir el enlace de restablecimiento
#        reset_link = f"http://localhost:5173/reset-password/?uid={uid}&token={token}"
#        # Nota: Reemplaza 'http://localhost:3000' con la URL de tu frontend en producción
#        
#        subject = "Restablecimiento de Contraseña"
#        message = render_to_string('password_reset_email.html', {
#            'user': user,
#            'reset_link': reset_link,
#        })
#
#        send_mail(
#            subject,
#            message,
#            settings.DEFAULT_FROM_EMAIL,
#            [email],
#            fail_silently=False,
#        )

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = UserModel.objects.get(email=value)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("No se encontró un usuario con ese correo electrónico.")
        return value

    def save(self):
        request = self.context.get('request')
        email = self.validated_data['email']
        user = UserModel.objects.get(email=email)
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Construir el enlace de restablecimiento
        reset_link = f"http://localhost:5173/reset-password/?uid={uid}&token={token}"
        # Nota: Reemplaza 'http://localhost:5173' con la URL de tu frontend en producción
        
        subject = "Restablecimiento de Contraseña"
        
        # Mensaje de texto plano
        plain_message = f"""Hola {user.username},Has solicitado restablecer tu contraseña. Por favor, haz clic en el siguiente enlace para establecer una nueva contraseña:{reset_link}Si no solicitaste este cambio, puedes ignorar este correo electrónico.Gracias,Tu Equipo"""
        # Mensaje HTML
        html_message = render_to_string('password_reset_email.html', {
            'user': user,
            'reset_link': reset_link,
        })

        send_mail(
            subject,
            plain_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
            html_message=html_message,  # Añade el mensaje HTML
        )

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Las contraseñas no coinciden."})

        # Validar la fuerza de la contraseña
        password = data['new_password']
        if len(password) < 8:
            raise serializers.ValidationError({"new_password": "La contraseña debe tener al menos 8 caracteres."})
        if not re.findall(r'\d', password):
            raise serializers.ValidationError({"new_password": "La contraseña debe contener al menos un número."})
        if not re.findall(r'[A-Z]', password):
            raise serializers.ValidationError({"new_password": "La contraseña debe contener al menos una letra mayúscula."})
        if not re.findall(r'[!@#$%^&*(),.?\":{}|<>]', password):
            raise serializers.ValidationError({"new_password": "La contraseña debe contener al menos un carácter especial."})
        
        # Decodificar el uid y obtener el usuario
        try:
            uid = force_str(urlsafe_base64_decode(data['uid']))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise serializers.ValidationError("El enlace de restablecimiento de contraseña es inválido.")

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("El enlace de restablecimiento de contraseña es inválido o ha expirado.")
        
        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
