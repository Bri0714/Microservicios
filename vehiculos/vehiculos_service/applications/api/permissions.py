#from rest_framework.permissions import BasePermission
#from django.conf import settings
#
#class IsOwner(BasePermission):
#    def has_permission(self, request, view):
#        # Permitir acciones de creación, listado y destrucción si el usuario está autenticado
#        if view.action in ['create', 'list', 'destroy']:
#            return request.user and request.user.is_authenticated
#        return True  # Puedes ajustar esto según tus necesidades
#
#    def has_object_permission(self, request, view, obj):
#        # Permitir al propietario del recurso acceder a él
#        return obj.user_id == request.user.id

# vehiculos/permissions.py y rutas/permissions.py

# rutas/applications/api/permissions.py

# vehiculos/applications/api/permissions.py

from rest_framework.permissions import BasePermission
from django.conf import settings

class IsOwnerOrServiceAccount(BasePermission):
    """
    Custom permission to allow access to the owner or the service account.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow access if the user is the owner
        if obj.user_id == request.user.id:
            return True

        # Allow access if the user is the service account
        if request.user.id == settings.SERVICE_ACCOUNT_USER_ID:
            return True

        return False
