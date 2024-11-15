from rest_framework import viewsets
from .models import Estudiante, Acudiente
from .serializers import EstudianteSerializer, AcudienteSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner

class AcudienteViewSet(viewsets.ModelViewSet):
    queryset = Acudiente.objects.all()
    serializer_class = AcudienteSerializer
    
    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        return Acudiente.objects.filter(user_id=user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
    
    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Estudiante.objects.filter(user_id=user.id)
        
        ruta_id = self.request.query_params.get('ruta_id', None)
        
        if ruta_id is not None:
            queryset = queryset.filter(ruta_id=ruta_id)
            
        colegio_id = self.request.query_params.get('colegio_id', None)
        
        if colegio_id is not None:
            queryset = queryset.filter(colegio_id=colegio_id)
            
        return queryset


    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
        