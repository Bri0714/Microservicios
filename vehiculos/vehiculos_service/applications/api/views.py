from rest_framework import viewsets
from .models import Vehiculo, Monitora
from .serializers import VehiculoSerializer, MonitoraSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response

class VehiculoListCreate(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Vehiculo.objects.filter(user_id=user.id)
        ruta_id = self.request.query_params.get('ruta_id', None)
        if ruta_id is not None:
            queryset = queryset.filter(ruta_id=ruta_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save()
    
class MonitoraListCreate(viewsets.ModelViewSet):
    queryset = Monitora.objects.all()
    serializer_class = MonitoraSerializer

    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Monitora.objects.filter(user_id=user.id)
        vehiculo_id = self.request.query_params.get('vehiculo_id', None)
        if vehiculo_id is not None:
            queryset = queryset.filter(vehiculo_id=vehiculo_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)