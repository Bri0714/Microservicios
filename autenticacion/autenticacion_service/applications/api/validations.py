from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def custom_validation(data):
    email = data.get('email', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not email:
        raise ValidationError('El campo de correo electrónico es obligatorio.')
    if UserModel.objects.filter(email=email).exists():
        raise ValidationError('El correo electrónico ya está registrado.')

    if not username:
        raise ValidationError('El campo de nombre de usuario es obligatorio.')
    if UserModel.objects.filter(username=username).exists():
        raise ValidationError('El nombre de usuario ya está registrado.')

    if not password or len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')

    return data


def validate_email(data):
    email = data.get('email', '').strip()
    if not email:
        raise ValidationError('Se requiere un correo electrónico.')
    return True

def validate_username(data):
    username = data.get('username', '').strip()
    if not username:
        raise ValidationError('El campo de nombre de usuario es obligatorio.')
    return True

def validate_password(data):
    password = data.get('password', '').strip()
    if not password:
        raise ValidationError('La contraseña es obligatoria.')
    if len(password) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
    return True
