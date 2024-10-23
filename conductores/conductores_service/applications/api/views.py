from rest_framework import viewsets
from .models import Conductor
from .serializers import ConductorSerializer

class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer