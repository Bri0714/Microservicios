# views.py
from rest_framework import viewsets
from .models import DocumentoVehiculo
from .serializers import DocumentoVehiculoSerializer
from rest_framework.permissions import IsAuthenticated
import requests
from .permissions import IsOwner
from datetime import date

class DocumentoVehiculoViewSet(viewsets.ModelViewSet):
    queryset = DocumentoVehiculo.objects.all()
    serializer_class = DocumentoVehiculoSerializer
    
    def get_permissions(self):
        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
        if self.action in ['create', 'list', 'destroy', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        # Filtrar documentos asociados a los vehículos del usuario
        queryset = DocumentoVehiculo.objects.filter(vehiculo_id__in=self._get_user_vehicle_ids(user.id))

        # Obtener parámetros de consulta
        vehiculo_id = self.request.query_params.get('vehiculo_id', None)
        tipo_documento = self.request.query_params.get('tipo_documento', None)

        # Aplicar filtros si se proporcionan
        if vehiculo_id is not None:
            queryset = queryset.filter(vehiculo_id=vehiculo_id)
        if tipo_documento is not None:
            queryset = queryset.filter(tipo_documento=tipo_documento)

        return queryset

    def perform_create(self, serializer):
        # Asociar el documento con el usuario autenticado
        serializer.save()
        self._actualizar_estado_ruta(serializer.validated_data['vehiculo_id'])

    def perform_update(self, serializer):
        # Actualizar el documento
        serializer.save()
        self._actualizar_estado_ruta(serializer.validated_data['vehiculo_id'])

    def perform_destroy(self, instance):
        # Eliminar el documento
        vehiculo_id = instance.vehiculo_id
        instance.delete()
        self._actualizar_estado_ruta(vehiculo_id)

    def _get_user_vehicle_ids(self, user_id):
        # Realizar una solicitud al microservicio de vehículos para obtener los IDs de vehículos que pertenecen al usuario autenticado
        headers = {'Authorization': self.request.headers.get('Authorization')}
        response = requests.get(f'http://vehiculos:8006/api/vehiculos/?user_id={user_id}', headers=headers)
        if response.status_code == 200:
            return [vehiculo['id'] for vehiculo in response.json()]
        return []

    def _actualizar_estado_ruta(self, vehiculo_id):
        # Verificar el estado de todos los documentos del vehículo
        documentos = DocumentoVehiculo.objects.filter(vehiculo_id=vehiculo_id)
        todos_vigentes = all(doc.estado == 'Vigente' for doc in documentos)

        # Obtener la ruta asociada al vehículo desde el microservicio de rutas y actualizar su estado
        headers = {'Authorization': self.request.headers.get('Authorization')}
        vehiculo_response = requests.get(f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers)

        if vehiculo_response.status_code == 200:
            vehiculo_data = vehiculo_response.json()
            ruta_id = vehiculo_data.get('ruta_id')

            if ruta_id is not None:
                # Actualizar el estado de la ruta asociada
                requests.patch(
                    f'http://rutas:8002/api/rutas/{ruta_id}/',
                    json={'activa': todos_vigentes},
                    headers=headers
                )
