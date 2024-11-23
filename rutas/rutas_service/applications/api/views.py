#from rest_framework import viewsets
#from .models import Ruta
#from .serializers import RutaSerializer
#from rest_framework.permissions import IsAuthenticated
#from .permissions import IsOwner
#import requests
#
#class RutaListCreate(viewsets.ModelViewSet):
#    queryset = Ruta.objects.all()
#    serializer_class = RutaSerializer
#
#    def get_permissions(self):
#        # Permitir crear, listar, actualizar y eliminar si el usuario está autenticado
#        if self.action in ['create', 'list', 'destroy', 'update']:
#            permission_classes = [IsAuthenticated]
#        else:
#            permission_classes = [IsAuthenticated, IsOwner]
#        return [permission() for permission in permission_classes]
#
#    def get_queryset(self):
#        user = self.request.user
#        return Ruta.objects.filter(user_id=user.id)
#
#    def perform_create(self, serializer):
#        serializer.save(user_id=self.request.user.id)
#
#    def _get_auth_headers(self):
#        request = self.request
#        token = request.headers.get('Authorization') if request else None
#        if not token:
#            raise Exception('No se pudo obtener el token de autorización.')
#        return {'Authorization': token}
#    
#    # Eliminar
#    def destroy(self, request, *args, **kwargs):
#        ruta = self.get_object()
#        ruta_id = ruta.id
#        headers = self._get_auth_headers()
#
#        # 1. Eliminar el Vehículo asociado a la Ruta
#        try:
#            vehiculo_response = requests.get(
#                f'http://vehiculos:8006/api/vehiculos/?ruta_id={ruta_id}', headers=headers
#            )
#            if vehiculo_response.status_code == 200:
#                vehiculos = vehiculo_response.json()
#                for vehiculo in vehiculos:
#                    vehiculo_id = vehiculo['id']
#                    # Eliminar el Conductor asociado al Vehículo
#                    conductor_response = requests.get(
#                        f'http://conductores:8005/api/conductores/?vehiculo_id={vehiculo_id}', headers=headers
#                    )
#                    if conductor_response.status_code == 200:
#                        conductores = conductor_response.json()
#                        for conductor in conductores:
#                            conductor_id = conductor['id']
#                            # Eliminar el Conductor
#                            delete_conductor_response = requests.delete(
#                                f'http://conductores:8005/api/conductores/{conductor_id}/', headers=headers
#                            )
#                    # Eliminar el Vehículo
#                    delete_vehiculo_response = requests.delete(
#                        f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers
#                    )
#        except Exception as e:
#            print(f'Error al eliminar el vehículo o conductor asociado: {e}')
#
#        # 2. Eliminar los Estudiantes asociados a la Ruta
#        try:
#            estudiantes_response = requests.get(
#                f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta_id}', headers=headers
#            )
#            if estudiantes_response.status_code == 200:
#                estudiantes = estudiantes_response.json()
#                for estudiante in estudiantes:
#                    estudiante_id = estudiante['id']
#                    # Eliminar el Estudiante
#                    delete_estudiante_response = requests.delete(
#                        f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/', headers=headers
#                    )
#        except Exception as e:
#            print(f'Error al eliminar los estudiantes asociados: {e}')
#
#        # 3. Eliminar la Ruta
#        response = super().destroy(request, *args, **kwargs)
#        return response
#    
#    # Actualizar  
#    def update(self, request, *args, **kwargs):
#        ruta = self.get_object()
#        headers = self._get_auth_headers()
#
#        # 1. Obtener la lista actual de instituciones_ids antes de la actualización
#        instituciones_ids_antes = set(ruta.instituciones_ids)
#
#        # 2. Obtener la nueva lista de instituciones_ids del request
#        instituciones_ids_nuevas = set(request.data.get('instituciones_ids', ruta.instituciones_ids))
#
#        # 3. Determinar las instituciones eliminadas
#        instituciones_eliminadas = instituciones_ids_antes - instituciones_ids_nuevas
#
#        # 4. Eliminar los estudiantes asociados a la ruta y a las instituciones eliminadas
#        for institucion_id in instituciones_eliminadas:
#            try:
#                estudiantes_response = requests.get(
#                    f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta.id}&colegio_id={institucion_id}',
#                    headers=headers
#                )
#                if estudiantes_response.status_code == 200:
#                    estudiantes = estudiantes_response.json()
#                    for estudiante in estudiantes:
#                        estudiante_id = estudiante['id']
#                        delete_estudiante_response = requests.delete(
#                            f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/',
#                            headers=headers
#                        )
#            except Exception as e:
#                print(f'Error al eliminar los estudiantes asociados a la institución {institucion_id}: {e}')
#
#        # 5. Actualizar la ruta con los nuevos datos
#        response = super().update(request, *args, **kwargs)
#        return response
#    # Eliminar
#    def destroy(self, request, *args, **kwargs):
#        ruta = self.get_object()
#        ruta_id = ruta.id
#        headers = self._get_auth_headers()
#
#        # 1. Eliminar el Vehículo asociado a la Ruta
#        try:
#            vehiculo_response = requests.get(
#                f'http://vehiculos:8006/api/vehiculos/?ruta_id={ruta_id}', headers=headers
#            )
#            if vehiculo_response.status_code == 200:
#                vehiculos = vehiculo_response.json()
#                for vehiculo in vehiculos:
#                    vehiculo_id = vehiculo['id']
#                    # Eliminar el Conductor asociado al Vehículo
#                    conductor_response = requests.get(
#                        f'http://conductores:8005/api/conductores/?vehiculo_id={vehiculo_id}', headers=headers
#                    )
#                    if conductor_response.status_code == 200:
#                        conductores = conductor_response.json()
#                        for conductor in conductores:
#                            conductor_id = conductor['id']
#                            # Eliminar el Conductor
#                            delete_conductor_response = requests.delete(
#                                f'http://conductores:8005/api/conductores/{conductor_id}/', headers=headers
#                            )
#                    # Eliminar el Vehículo
#                    delete_vehiculo_response = requests.delete(
#                        f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers
#                    )
#        except Exception as e:
#            print(f'Error al eliminar el vehículo o conductor asociado: {e}')
#
#        # 2. Eliminar los Estudiantes asociados a la Ruta
#        try:
#            estudiantes_response = requests.get(
#                f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta_id}', headers=headers
#            )
#            if estudiantes_response.status_code == 200:
#                estudiantes = estudiantes_response.json()
#                for estudiante in estudiantes:
#                    estudiante_id = estudiante['id']
#                    # Eliminar el Estudiante
#                    delete_estudiante_response = requests.delete(
#                        f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/', headers=headers
#                    )
#        except Exception as e:
#            print(f'Error al eliminar los estudiantes asociados: {e}')
#
#        # 3. Eliminar la Ruta
#        response = super().destroy(request, *args, **kwargs)
#        return response
#    
#    # Actualizar  
#    def update(self, request, *args, **kwargs):
#        ruta = self.get_object()
#        headers = self._get_auth_headers()
#
#        # 1. Obtener la lista actual de instituciones_ids antes de la actualización
#        instituciones_ids_antes = set(ruta.instituciones_ids)
#
#        # 2. Obtener la nueva lista de instituciones_ids del request
#        instituciones_ids_nuevas = set(request.data.get('instituciones_ids', ruta.instituciones_ids))
#
#        # 3. Determinar las instituciones eliminadas
#        instituciones_eliminadas = instituciones_ids_antes - instituciones_ids_nuevas
#
#        # 4. Eliminar los estudiantes asociados a la ruta y a las instituciones eliminadas
#        for institucion_id in instituciones_eliminadas:
#            try:
#                estudiantes_response = requests.get(
#                    f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta.id}&colegio_id={institucion_id}',
#                    headers=headers
#                )
#                if estudiantes_response.status_code == 200:
#                    estudiantes = estudiantes_response.json()
#                    for estudiante in estudiantes:
#                        estudiante_id = estudiante['id']
#                        delete_estudiante_response = requests.delete(
#                            f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/',
#                            headers=headers
#                        )
#            except Exception as e:
#                print(f'Error al eliminar los estudiantes asociados a la institución {institucion_id}: {e}')
#
#        # 5. Actualizar la ruta con los nuevos datos
#        response = super().update(request, *args, **kwargs)
#        return response

# rutas/applications/api/views.py

from rest_framework import viewsets
from .models import Ruta
from .serializers import RutaSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrServiceAccount
import requests
from django.conf import settings

class RutaListCreate(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

    def get_permissions(self):
        permission_classes = [IsAuthenticated, IsOwnerOrServiceAccount]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user
        if user.id == settings.SERVICE_ACCOUNT_USER_ID:
            # Service account can access all routes
            return Ruta.objects.all()
        else:
            return Ruta.objects.filter(user_id=user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def _get_auth_headers(self):
        request = self.request
        token = request.headers.get('Authorization') if request else None
        if not token:
            raise Exception('No se pudo obtener el token de autorización.')
        return {'Authorization': token}

    # Rest of your code remains unchanged...
    # Eliminar
    def destroy(self, request, *args, **kwargs):
        ruta = self.get_object()
        ruta_id = ruta.id
        headers = self._get_auth_headers()

        # 1. Eliminar el Vehículo asociado a la Ruta
        try:
            vehiculo_response = requests.get(
                f'http://vehiculos:8006/api/vehiculos/?ruta_id={ruta_id}', headers=headers
            )
            if vehiculo_response.status_code == 200:
                vehiculos = vehiculo_response.json()
                for vehiculo in vehiculos:
                    vehiculo_id = vehiculo['id']
                    # Eliminar el Conductor asociado al Vehículo
                    conductor_response = requests.get(
                        f'http://conductores:8005/api/conductores/?vehiculo_id={vehiculo_id}', headers=headers
                    )
                    if conductor_response.status_code == 200:
                        conductores = conductor_response.json()
                        for conductor in conductores:
                            conductor_id = conductor['id']
                            # Eliminar el Conductor
                            delete_conductor_response = requests.delete(
                                f'http://conductores:8005/api/conductores/{conductor_id}/', headers=headers
                            )
                    # Eliminar el Vehículo
                    delete_vehiculo_response = requests.delete(
                        f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers
                    )
        except Exception as e:
            print(f'Error al eliminar el vehículo o conductor asociado: {e}')

        # 2. Eliminar los Estudiantes asociados a la Ruta
        try:
            estudiantes_response = requests.get(
                f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta_id}', headers=headers
            )
            if estudiantes_response.status_code == 200:
                estudiantes = estudiantes_response.json()
                for estudiante in estudiantes:
                    estudiante_id = estudiante['id']
                    # Eliminar el Estudiante
                    delete_estudiante_response = requests.delete(
                        f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/', headers=headers
                    )
        except Exception as e:
            print(f'Error al eliminar los estudiantes asociados: {e}')

        # 3. Eliminar la Ruta
        response = super().destroy(request, *args, **kwargs)
        return response
    
    # Actualizar  
    def update(self, request, *args, **kwargs):
        ruta = self.get_object()
        headers = self._get_auth_headers()

        # 1. Obtener la lista actual de instituciones_ids antes de la actualización
        instituciones_ids_antes = set(ruta.instituciones_ids)

        # 2. Obtener la nueva lista de instituciones_ids del request
        instituciones_ids_nuevas = set(request.data.get('instituciones_ids', ruta.instituciones_ids))

        # 3. Determinar las instituciones eliminadas
        instituciones_eliminadas = instituciones_ids_antes - instituciones_ids_nuevas

        # 4. Eliminar los estudiantes asociados a la ruta y a las instituciones eliminadas
        for institucion_id in instituciones_eliminadas:
            try:
                estudiantes_response = requests.get(
                    f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta.id}&colegio_id={institucion_id}',
                    headers=headers
                )
                if estudiantes_response.status_code == 200:
                    estudiantes = estudiantes_response.json()
                    for estudiante in estudiantes:
                        estudiante_id = estudiante['id']
                        delete_estudiante_response = requests.delete(
                            f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/',
                            headers=headers
                        )
            except Exception as e:
                print(f'Error al eliminar los estudiantes asociados a la institución {institucion_id}: {e}')

        # 5. Actualizar la ruta con los nuevos datos
        response = super().update(request, *args, **kwargs)
        return response
    # Eliminar
    def destroy(self, request, *args, **kwargs):
        ruta = self.get_object()
        ruta_id = ruta.id
        headers = self._get_auth_headers()

        # 1. Eliminar el Vehículo asociado a la Ruta
        try:
            vehiculo_response = requests.get(
                f'http://vehiculos:8006/api/vehiculos/?ruta_id={ruta_id}', headers=headers
            )
            if vehiculo_response.status_code == 200:
                vehiculos = vehiculo_response.json()
                for vehiculo in vehiculos:
                    vehiculo_id = vehiculo['id']
                    # Eliminar el Conductor asociado al Vehículo
                    conductor_response = requests.get(
                        f'http://conductores:8005/api/conductores/?vehiculo_id={vehiculo_id}', headers=headers
                    )
                    if conductor_response.status_code == 200:
                        conductores = conductor_response.json()
                        for conductor in conductores:
                            conductor_id = conductor['id']
                            # Eliminar el Conductor
                            delete_conductor_response = requests.delete(
                                f'http://conductores:8005/api/conductores/{conductor_id}/', headers=headers
                            )
                    # Eliminar el Vehículo
                    delete_vehiculo_response = requests.delete(
                        f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers
                    )
        except Exception as e:
            print(f'Error al eliminar el vehículo o conductor asociado: {e}')

        # 2. Eliminar los Estudiantes asociados a la Ruta
        try:
            estudiantes_response = requests.get(
                f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta_id}', headers=headers
            )
            if estudiantes_response.status_code == 200:
                estudiantes = estudiantes_response.json()
                for estudiante in estudiantes:
                    estudiante_id = estudiante['id']
                    # Eliminar el Estudiante
                    delete_estudiante_response = requests.delete(
                        f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/', headers=headers
                    )
        except Exception as e:
            print(f'Error al eliminar los estudiantes asociados: {e}')

        # 3. Eliminar la Ruta
        response = super().destroy(request, *args, **kwargs)
        return response
    
    # Actualizar  
    def update(self, request, *args, **kwargs):
        ruta = self.get_object()
        headers = self._get_auth_headers()

        # 1. Obtener la lista actual de instituciones_ids antes de la actualización
        instituciones_ids_antes = set(ruta.instituciones_ids)

        # 2. Obtener la nueva lista de instituciones_ids del request
        instituciones_ids_nuevas = set(request.data.get('instituciones_ids', ruta.instituciones_ids))

        # 3. Determinar las instituciones eliminadas
        instituciones_eliminadas = instituciones_ids_antes - instituciones_ids_nuevas

        # 4. Eliminar los estudiantes asociados a la ruta y a las instituciones eliminadas
        for institucion_id in instituciones_eliminadas:
            try:
                estudiantes_response = requests.get(
                    f'http://estudiantes:8004/api/estudiantes/?ruta_id={ruta.id}&colegio_id={institucion_id}',
                    headers=headers
                )
                if estudiantes_response.status_code == 200:
                    estudiantes = estudiantes_response.json()
                    for estudiante in estudiantes:
                        estudiante_id = estudiante['id']
                        delete_estudiante_response = requests.delete(
                            f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/',
                            headers=headers
                        )
            except Exception as e:
                print(f'Error al eliminar los estudiantes asociados a la institución {institucion_id}: {e}')

        # 5. Actualizar la ruta con los nuevos datos
        response = super().update(request, *args, **kwargs)
        return response