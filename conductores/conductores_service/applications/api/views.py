from rest_framework import viewsets
from .models import Conductor
from .serializers import ConductorSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

class ConductorViewSet(viewsets.ModelViewSet):
    
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer
    
    
    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        return Conductor.objects.filter(user_id=user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)


