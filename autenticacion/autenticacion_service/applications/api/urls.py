# applications/api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, LoginView, LogoutView, CurrentUserView, UpdateProfileView, PasswordResetRequestView, PasswordResetConfirmView
#UserViewSet

router = DefaultRouter()
#router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/users/current_user/', CurrentUserView.as_view(), name='current_user'),
    path('api/users/update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    # Rutas para restablecimiento de contraseña
    path('api/password_reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('api/password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]

