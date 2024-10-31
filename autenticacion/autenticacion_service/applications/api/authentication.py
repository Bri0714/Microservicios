# autenticacion/authentication.py

import jwt
from rest_framework import authentication, exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = authentication.get_authorization_header(request)
        if not auth_header:
            return None  # No se proporciona token

        try:
            prefix, token = auth_header.decode('utf-8').split(' ')
            if prefix.lower() != 'bearer':
                return None
        except ValueError:
            return None

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.objects.get(user_id=user_id)
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('El token ha expirado.')
        except (jwt.InvalidTokenError, User.DoesNotExist):
            raise exceptions.AuthenticationFailed('Token inválido o usuario no encontrado.')

        return (user, token)
