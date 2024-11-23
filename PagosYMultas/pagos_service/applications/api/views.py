from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Pago
from .serializers import PagoSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerPago
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework.exceptions import ValidationError  # Importar ValidationError

class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.all()
    serializer_class = PagoSerializer
    permission_classes = [IsAuthenticated, IsOwnerPago]

    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update', 'partial_update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwnerPago]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        queryset = Pago.objects.filter(user_id=user.id)
        request = self.request

        # Obtener parámetros de consulta
        estudiante_id = request.query_params.get('estudiante_id', None)
        mes_a_pagar = request.query_params.get('mes_a_pagar', None)
        numero_talonario = request.query_params.get('numero_talonario', None)

        # Filtrar por estudiante_id si está presente
        if estudiante_id is not None:
            try:
                estudiante_id = int(estudiante_id)
                queryset = queryset.filter(estudiante_id=estudiante_id)
            except ValueError:
                raise ValidationError({"estudiante_id": "El ID del estudiante debe ser un número entero."})

        # Filtrar por mes_a_pagar si está presente
        if mes_a_pagar is not None:
            queryset = queryset.filter(mes_a_pagar=mes_a_pagar)

        # Filtrar por numero_talonario si está presente
        if numero_talonario is not None:
            queryset = queryset.filter(numero_talonario=numero_talonario)

        return queryset

    def perform_create(self, serializer):
        # Asignar user_id desde el usuario autenticado
        serializer.save(user_id=self.request.user.id)

    def perform_update(self, serializer):
        # Asegurar que user_id no sea modificado durante la actualización
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsOwnerPago])
    def pagar(self, request, pk=None):
        pago = self.get_object()
        if pago.fecha_de_pago:
            return Response({'detail': 'Este pago ya ha sido registrado.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Registrar la fecha de pago y recalcular multas y estado_pago
        serializer = self.get_serializer(pago, data={'fecha_de_pago': timezone.now().date()}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
