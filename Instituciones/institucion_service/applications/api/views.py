from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Institucion
from .serializers import InstitucionSerializer
from .permissions import IsOwner

class InstitucionViewSet(viewsets.ModelViewSet):
    serializer_class = InstitucionSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        user = self.request.user
        print("Usuario autenticado:", user)
        print("ID del usuario:", user.id)
        return Institucion.objects.filter(user_id=user.id)


    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)
