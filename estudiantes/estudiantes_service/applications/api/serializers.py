# serializers.py

from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer
from .models import Estudiante, Acudiente
import requests
from rest_framework.serializers import ValidationError


class AcudienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Acudiente
        fields = '__all__'
        read_only_fields = ['id', 'user_id']

class EstudianteSerializer(WritableNestedModelSerializer):
    acudiente = AcudienteSerializer()
    institucion = serializers.SerializerMethodField()
    ruta = serializers.SerializerMethodField()

    class Meta:
        model = Estudiante
        fields = [
            'id', 'acudiente', 'estudiante_foto', 'colegio_id', 'ruta_id',
            'estudiante_nombre', 'estudiante_apellido', 'estudiante_edad',
            'estudiante_curso', 'estudiante_direccion', 'estudiante_fecha_ingreso_ruta',
            'estudiante_estado', 'institucion', 'ruta'
        ]
        read_only_fields = ['id', 'user_id', 'estudiante_estado', 'institucion', 'ruta']

    def _get_auth_headers(self):
        """
        Obtiene el token JWT del contexto de la solicitud y lo agrega en el encabezado de autorización.
        """
        request = self.context.get('request')
        token = request.headers.get('Authorization') if request else None
        if not token:
            raise serializers.ValidationError('No se pudo obtener el token de autorización.')
        return {'Authorization': token}

    def validate_colegio_id(self, value):
        """
        Valida que la institución con el ID proporcionado exista.
        """
        headers = self._get_auth_headers()
        response = requests.get(f'http://instituciones:8001/api/instituciones/{value}/', headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError(f'La institución con ID {value} no existe o no se pudo verificar.')
        return value

    def validate_ruta_id(self, value):
        """
        Valida que la ruta con el ID proporcionado exista.
        """
        headers = self._get_auth_headers()
        response = requests.get(f'http://rutas:8002/api/rutas/{value}/', headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError(f'La ruta con ID {value} no existe o no se pudo verificar.')
        return value

    def create(self, validated_data):
        """
        Crea un estudiante y su acudiente asociado, asegurando que la ruta y la institución existan y estén asociadas.
        """
        # Extraer y manejar los datos de Acudiente
        acudiente_data = validated_data.pop('acudiente')

        # Obtener el user_id del contexto de la solicitud
        user_id = self.context['request'].user.id
        acudiente_data['user_id'] = user_id

        # Verificar si el acudiente ya existe basado en el número de teléfono y user_id
        acudiente_telefono = acudiente_data.get('acudiente_telefono')
        acudiente = Acudiente.objects.filter(acudiente_telefono=acudiente_telefono, user_id=user_id).first()

        if not acudiente:
            # Si no existe, crear el acudiente
            acudiente = Acudiente.objects.create(**acudiente_data)

        # Verificar si la ruta está asociada a la institución especificada
        colegio_id = validated_data.get('colegio_id')
        ruta_id = validated_data.get('ruta_id')

        headers = self._get_auth_headers()

        # Verificar existencia de la ruta
        ruta_response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
        if ruta_response.status_code != 200:
            raise serializers.ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')

        ruta_data = ruta_response.json()
        if colegio_id not in ruta_data.get('instituciones_ids', []):
            raise serializers.ValidationError(f'La ruta con ID {ruta_id} no está asociada a la institución con ID {colegio_id}.')

        # Verificar que la ruta tenga un vehículo asociado
        vehiculo_response = requests.get(f'http://vehiculos:8006/api/vehiculos/', headers=headers)
        if vehiculo_response.status_code != 200:
            raise serializers.ValidationError(f'Error al verificar el vehículo asociado a la ruta con ID {ruta_id}.')

        vehiculos = vehiculo_response.json()
        # Filtrar los vehículos por ruta_id
        vehiculos_ruta = [v for v in vehiculos if v.get('ruta_id') == ruta_id]

        if not vehiculos_ruta:
            raise serializers.ValidationError(f'La ruta con ID {ruta_id} no tiene un vehículo asociado.')

        # Asumiendo que solo hay un vehículo por ruta
        vehiculo_data = vehiculos_ruta[0]
        capacidad = vehiculo_data.get("vehiculo_capacidad")
        if capacidad is None:
            raise serializers.ValidationError(f'El vehículo asociado a la ruta con ID {ruta_id} no tiene definida su capacidad.')

        # Contar estudiantes actualmente en la ruta
        estudiantes_en_ruta = Estudiante.objects.filter(ruta_id=ruta_id).count()
        if estudiantes_en_ruta >= capacidad:
            raise serializers.ValidationError(
                f'El vehículo asociado a la ruta con ID {ruta_id} ya ha alcanzado su capacidad máxima de {capacidad} estudiantes. No se pueden agregar más estudiantes a esta ruta.'
            )

        # Agregar user_id al validated_data
        validated_data['user_id'] = user_id

        # Crear el estudiante con el acudiente relacionado
        estudiante = Estudiante.objects.create(acudiente=acudiente, **validated_data)
        return estudiante

    def update(self, instance, validated_data):
        """
        Actualiza un estudiante y su acudiente asociado, asegurando que la ruta y la institución existan y estén asociadas.
        """
        # Extraer y manejar los datos de Acudiente
        acudiente_data = validated_data.pop('acudiente', None)
        if acudiente_data:
            acudiente_telefono = acudiente_data.get('acudiente_telefono')
            user_id = self.context['request'].user.id
            acudiente_data['user_id'] = user_id

            acudiente = Acudiente.objects.filter(acudiente_telefono=acudiente_telefono, user_id=user_id).first()
            if not acudiente:
                acudiente = Acudiente.objects.create(**acudiente_data)
            instance.acudiente = acudiente

        # Verificar si la ruta está asociada a la institución especificada
        colegio_id = validated_data.get('colegio_id', instance.colegio_id)
        ruta_id = validated_data.get('ruta_id', instance.ruta_id)

        headers = self._get_auth_headers()

        # Verificar existencia de la ruta
        ruta_response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
        if ruta_response.status_code != 200:
            raise serializers.ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')

        ruta_data = ruta_response.json()
        if colegio_id not in ruta_data.get('instituciones_ids', []):
            raise serializers.ValidationError(f'La ruta con ID {ruta_id} no está asociada a la institución con ID {colegio_id}.')

        # Verificar que la ruta tenga un vehículo asociado
        vehiculo_response = requests.get(f'http://vehiculos:8006/api/vehiculos/', headers=headers)
        if vehiculo_response.status_code != 200:
            raise serializers.ValidationError(f'Error al verificar el vehículo asociado a la ruta con ID {ruta_id}.')

        vehiculos = vehiculo_response.json()
        # Filtrar los vehículos por ruta_id
        vehiculos_ruta = [v for v in vehiculos if v.get('ruta_id') == ruta_id]

        if not vehiculos_ruta:
            raise serializers.ValidationError(f'La ruta con ID {ruta_id} no tiene un vehículo asociado.')

        # Verificar capacidad del vehículo asociado a la ruta si la ruta cambia
        if ruta_id != instance.ruta_id:
            vehiculo_data = vehiculos_ruta[0]  # Asumiendo que solo hay un vehículo por ruta
            capacidad = vehiculo_data.get("vehiculo_capacidad")
            if capacidad is None:
                raise serializers.ValidationError(f'El vehículo asociado a la ruta con ID {ruta_id} no tiene definida su capacidad.')

            # Contar estudiantes actualmente en la nueva ruta
            estudiantes_en_ruta = Estudiante.objects.filter(ruta_id=ruta_id).count()
            if estudiantes_en_ruta >= capacidad:
                raise serializers.ValidationError(
                    f'El vehículo asociado a la ruta con ID {ruta_id} ya ha alcanzado su capacidad máxima de {capacidad} estudiantes. No se pueden agregar más estudiantes a esta ruta.'
                )

        # Agregar user_id al validated_data
        validated_data['user_id'] = self.context['request'].user.id

        # Actualizar los datos del estudiante
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def get_institucion(self, obj):
        """
        Devuelve el ID y el nombre de la institución asociada.
        """
        headers = self._get_auth_headers()
        response = requests.get(f'http://instituciones:8001/api/instituciones/{obj.colegio_id}/', headers=headers)
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
        headers = self._get_auth_headers()
        response = requests.get(f'http://rutas:8002/api/rutas/{obj.ruta_id}/', headers=headers)
        if response.status_code == 200:
            ruta_data = response.json()
            return {
                'id': ruta_data.get('id'),
                'nombre': ruta_data.get('ruta_nombre')
            }
        return None
