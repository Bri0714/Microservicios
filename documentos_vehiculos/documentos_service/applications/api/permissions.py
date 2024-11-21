from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_permission(self, request, view):
        # Permitir acciones de creación, listado y destrucción si el usuario está autenticado
        if view.action in ['create', 'list', 'destroy']:
            return request.user and request.user.is_authenticated
        return True  # Puedes ajustar esto según tus necesidades

    def has_object_permission(self, request, view, obj):
        # Permitir al propietario del recurso acceder a él
        return obj.user_id == request.user.id
