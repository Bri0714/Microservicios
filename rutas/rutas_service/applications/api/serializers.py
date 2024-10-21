from rest_framework import serializers
from .models import Ruta
import requests
from django.core.exceptions import ValidationError

class RutaSerializer(serializers.ModelSerializer):
    institucion = serializers.SerializerMethodField()

    class Meta:
        model = Ruta
        fields = '__all__'

    def validate_institucion_id(self, value):
        """
        Valida que la institución con el ID proporcionado exista.
        """
        response = requests.get(f'http://instituciones:8001/api/instituciones/{value}/')
        if response.status_code != 200:
            raise ValidationError(f'La institución con ID {value} no existe.')
        return value

    def get_institucion(self, obj):
        """
        Devuelve el ID y el nombre de la institución asociada.
        """
        response = requests.get(f'http://instituciones:8001/api/instituciones/{obj.institucion_id}/')
        if response.status_code == 200:
            institucion_data = response.json()
            return {
                'id': institucion_data.get('id'),
                'nombre': institucion_data.get('institucion_nombre')
            }
        return None

    def create(self, validated_data):
        """
        Se asegura de que la institución existe antes de crear la ruta.
        """
        institucion_id = validated_data.get('institucion_id')
        response = requests.get(f'http://instituciones:8001/api/instituciones/{institucion_id}/')
        if response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia de la institución con ID {institucion_id}.')
        return super().create(validated_data)
