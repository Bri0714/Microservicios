from rest_framework import serializers
from .models import Ruta
import requests
from django.core.exceptions import ValidationError

class RutaSerializer(serializers.ModelSerializer):
    instituciones = serializers.SerializerMethodField()  # Devuelve información sobre las instituciones relacionadas

    class Meta:
        model = Ruta
        fields = '__all__'
        read_only_fields = ['id', 'user_id']

    def _get_auth_headers(self):
        """
        Obtiene el token JWT del request context y lo agrega en el encabezado de autorización.
        """
        request = self.context.get('request')
        token = request.headers.get('Authorization') if request else None
        if not token:
            raise ValidationError('No se pudo obtener el token de autorización.')
        return {'Authorization': token}

    def validate_instituciones_ids(self, value):
        """
        Valida que cada institución con los IDs proporcionados exista.
        """
        request = self.context.get('request')
        if request and request.method in ['POST', 'PUT']:  # Solo validar en creación o actualización
            if not isinstance(value, list):
                raise ValidationError('El campo instituciones_ids debe ser una lista de IDs.')

            headers = self._get_auth_headers()
            for institucion_id in value:
                response = requests.get(
                    f'http://instituciones:8001/api/instituciones/{institucion_id}/', headers=headers
                )
                if response.status_code != 200:
                    raise ValidationError(f'La institución con ID {institucion_id} no existe.')
        return value

    def get_instituciones(self, obj):
        """
        Devuelve los detalles de las instituciones asociadas.
        """
        instituciones = []
        headers = self._get_auth_headers()
        for institucion_id in obj.instituciones_ids:
            response = requests.get(
                f'http://instituciones:8001/api/instituciones/{institucion_id}/', headers=headers
            )
            if response.status_code == 200:
                institucion_data = response.json()
                instituciones.append({
                    'id': institucion_data.get('id'),
                    'nombre': institucion_data.get('institucion_nombre')
                })
        return instituciones

    def create(self, validated_data):
        """
        Se asegura de que las instituciones existen antes de crear la ruta.
        """
        instituciones_ids = validated_data.get('instituciones_ids', [])
        headers = self._get_auth_headers()#
        for institucion_id in instituciones_ids:
            response = requests.get(
                f'http://instituciones:8001/api/instituciones/{institucion_id}/', headers=headers
            )
            if response.status_code != 200:
                raise ValidationError(f'No se pudo verificar la existencia de la institución con ID {institucion_id}.')
        
        return super().create(validated_data)#
    def update(self, instance, validated_data):
        """
        Se asegura de que las instituciones existen antes de actualizar la ruta.
        """
        instituciones_ids = validated_data.get('instituciones_ids', instance.instituciones_ids)
        headers = self._get_auth_headers()#
        for institucion_id in instituciones_ids:
            response = requests.get(
                f'http://instituciones:8001/api/instituciones/{institucion_id}/', headers=headers
            )
            if response.status_code != 200:
                raise ValidationError(f'No se pudo verificar la existencia de la institución con ID {institucion_id}.')#
        instance.ruta_nombre = validated_data.get('ruta_nombre', instance.ruta_nombre)
        instance.ruta_movil = validated_data.get('ruta_movil', instance.ruta_movil)
        instance.activa = validated_data.get('activa', instance.activa)
        instance.instituciones_ids = instituciones_ids
        instance.save()
        return instance
    