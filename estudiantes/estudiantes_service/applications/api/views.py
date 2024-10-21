from rest_framework import viewsets
from .models import Estudiante, Acudiente
from .serializers import EstudianteSerializer, AcudienteSerializer

class AcudienteViewSet(viewsets.ModelViewSet):
    queryset = Acudiente.objects.all()
    serializer_class = AcudienteSerializer

class EstudianteViewSet(viewsets.ModelViewSet):
    queryset = Estudiante.objects.all()
    serializer_class = EstudianteSerializer
