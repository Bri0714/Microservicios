from rest_framework import viewsets
from .models import Ruta
from .serializers import RutaSerializer


class RutaListCreate(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer
