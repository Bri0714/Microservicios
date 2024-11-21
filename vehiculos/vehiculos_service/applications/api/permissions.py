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

# vehiculos/permissions.py y rutas/permissions.py

# vehiculos_service/applications/api/permissions.py y rutas_service/applications/api/permissions.py

class IsServiceAccountOrOwner(BasePermission):
    """
    Permite el acceso si el usuario es la cuenta de servicio o el propietario del recurso.
    """
    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica si el usuario es la cuenta de servicio usando 'username'
        if hasattr(request.user, 'username') and request.user.username == 'service_account':
            return True
        
        # De lo contrario, permite que los usuarios autenticados accedan a las acciones permitidas
        return True
    
    def has_object_permission(self, request, view, obj):
        # Permite acceso completo a la cuenta de servicio
        if hasattr(request.user, 'username') and request.user.username == 'service_account':
            return True
        
        # De lo contrario, verifica si el usuario es el propietario
        return obj.user_id == request.user.user_id

