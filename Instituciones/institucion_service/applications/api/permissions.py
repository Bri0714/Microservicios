# instituciones/permissions.py

from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        # Permitir acciones de creación y listado
        if view.action in ['create', 'list']:
            return True
        return True  # Puedes ajustar esto según tus necesidades

    def has_object_permission(self, request, view, obj):
        return obj.user_id == request.user.id
