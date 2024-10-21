from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Estudiante, Acudiente
import requests
from django.core.exceptions import ValidationError

class AcudienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acudiente
        fields = '__all__'

class EstudianteSerializer(WritableNestedModelSerializer):
    acudiente = AcudienteSerializer()

    class Meta:
        model = Estudiante
        fields = [
            'id', 'acudiente', 'estudiante_foto', 'colegio_id', 'ruta_id',
            'estudiante_nombre', 'estudiante_apellido',
            'estudiante_edad', 'estudiante_curso' , 'estudiante_direccion'
        ]

    def create(self, validated_data):
        # Extraer y manejar los datos de Acudiente
        acudiente_data = validated_data.pop('acudiente')

        # Verificar si el acudiente ya existe basado en el número de teléfono
        acudiente_telefono = acudiente_data.get('acudiente_telefono')
        acudiente = Acudiente.objects.filter(acudiente_telefono=acudiente_telefono).first()

        if not acudiente:
            # Si no existe, crear el acudiente
            acudiente = Acudiente.objects.create(**acudiente_data)

        # Crear el estudiante con el acudiente relacionado
        estudiante = Estudiante.objects.create(acudiente=acudiente, **validated_data)
        return estudiante


    def validate_colegio_id(self, value):
        """
        Valida que la institución con el ID proporcionado exista.
        """
        response = requests.get(f'http://instituciones:8001/api/instituciones/{value}/')
        if response.status_code != 200:
            raise ValidationError(f'La institución con ID {value} no existe.')
        return value

    def validate_ruta_id(self, value):
        """
        Valida que la ruta con el ID proporcionado exista.
        """
        response = requests.get(f'http://rutas:8002/api/rutas/{value}/')
        if response.status_code != 200:
            raise ValidationError(f'La ruta con ID {value} no existe.')
        return value

    def get_institucion(self, obj):
        """
        Devuelve el ID y el nombre de la institución asociada.
        """
        response = requests.get(f'http://instituciones:8001/api/instituciones/{obj.colegio_id}/')
        if response.status_code == 200:
            institucion_data = response.json()
            return {
                'id': institucion_data.get('id'),
                'nombre': institucion_data.get('institucion_nombre')
            }
        return None

    def get_ruta(self, obj):
        """
        Devuelve el ID y el nombre de la ruta asociada.
        """
        response = requests.get(f'http://rutas:8002/api/rutas/{obj.ruta_id}/')
        if response.status_code == 200:
            ruta_data = response.json()
            return {
                'id': ruta_data.get('id'),
                'nombre': ruta_data.get('ruta_nombre')
            }
        return None

    def create_colegio_ruta(self, validated_data):
        """
        Se asegura de que la institución y la ruta existen antes de crear el estudiante.
        """
        colegio_id = validated_data.get('colegio_id')
        ruta_id = validated_data.get('ruta_id')

        institucion_response = requests.get(f'http://instituciones:8001/api/instituciones/{colegio_id}/')
        if institucion_response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia de la institución con ID {colegio_id}.')

        ruta_response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/')
        if ruta_response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')

        return super().create(validated_data)
