# local.py

from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'autenticacion']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'autenticacion',
        'USER': 'brian',
        'PASSWORD': 'parada2023',
        'HOST': 'db_autenticacion',
        'PORT': '5432',
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://localhost',
    'http://127.0.0.1',
    'http://0.0.0.0',
]

CORS_ALLOW_CREDENTIALS = False  # Ya no necesitamos credenciales (cookies)

# Si no usas CSRF, puedes eliminar estas configuraciones
# CSRF_TRUSTED_ORIGINS = [
#     'http://localhost:5173',
#     'http://127.0.0.1',
#     'http://localhost',
# ]

# CSRF_COOKIE_HTTPONLY = False
# CSRF_COOKIE_SAMESITE = 'Lax'
# CSRF_COOKIE_SECURE = False

# Puedes eliminar las configuraciones de SESSION_COOKIE si no usas sesiones
# SESSION_COOKIE_SAMESITE = 'Lax'
# SESSION_COOKIE_SECURE = False
# SESSION_COOKIE_HTTPONLY = True
