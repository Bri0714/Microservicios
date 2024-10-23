from rest_framework import viewsets
from .models import Conductor
from .serializers import Conductorserializer

class InstitucionViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = Conductorserializer