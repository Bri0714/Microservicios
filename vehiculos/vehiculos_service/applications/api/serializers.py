from rest_framework import serializers
from .models import Vehiculo, Monitora
import requests
from django.core.exceptions import ValidationError
from drf_writable_nested import WritableNestedModelSerializer

class MonitoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitora
        fields = '__all__'
        read_only_fields = ['id', 'user_id', 'vehiculo']

class VehiculoSerializer(WritableNestedModelSerializer):
    monitora = MonitoraSerializer(required=False, allow_null=True)

    class Meta:
        model = Vehiculo
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
    
    def validate(self, attrs):
        user_id = self.context['request'].user.id
        vehiculo_placa = attrs.get('vehiculo_placa')
        ruta_id = attrs.get('ruta_id')

        vehiculo_id = self.instance.id if self.instance else None

        # Verificar unicidad de vehiculo_placa por usuario
        if Vehiculo.objects.filter(
            user_id=user_id,
            vehiculo_placa=vehiculo_placa
        ).exclude(id=vehiculo_id).exists():
            raise serializers.ValidationError({
                'vehiculo_placa': 'Ya existe un vehículo con esta placa para este usuario.'
            })

        # Verificar unicidad de ruta_id por usuario
        if Vehiculo.objects.filter(
            user_id=user_id,
            ruta_id=ruta_id
        ).exclude(id=vehiculo_id).exists():
            raise serializers.ValidationError({
                'ruta_id': 'Ya existe un vehículo asociado a esta ruta para este usuario.'
            })

        # Validar que la ruta existe en el microservicio
        headers = self._get_auth_headers()
        response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError({
                'ruta_id': f'La ruta con ID {ruta_id} no existe o no se pudo verificar.'
            })

        return attrs


    def validate_ruta_id(self, value):
        """
        Valida que la ruta con el ID proporcionado exista.
        """
        headers = self._get_auth_headers()
        response = requests.get(f'http://rutas:8002/api/rutas/{value}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'La ruta con ID {value} no existe o no se pudo verificar.')
        return value

    #def create(self, validated_data):
    #    """
    #    Se asegura de que la ruta existe antes de crear el vehículo.
    #    """
    #    validated_data['user_id'] = self.context['request'].user.id
    #    vehiculo = super().create(validated_data)
    #    ruta_id = validated_data.get('ruta_id')
    #    headers = self._get_auth_headers()
    #    
    #    response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
    #    if response.status_code != 200:
    #        raise ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')
#
    #    validated_data['user_id'] = self.context['request'].user.id
    #    monitora_data = validated_data.pop('monitora', None)
    #    vehiculo = super().create(validated_data)
#
    #    if monitora_data:
    #        monitora_data['user_id'] = self.context['request'].user.id
    #        Monitora.objects.create(vehiculo=vehiculo, **monitora_data)
#
    #    return vehiculo

    def create(self, validated_data):
        """
        Se asegura de que la ruta existe antes de crear el vehículo.
        """
        # Validar que la ruta existe antes de crear el vehículo
        ruta_id = validated_data.get('ruta_id')
        headers = self._get_auth_headers()
        response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')

        # Asignar user_id al validated_data
        validated_data['user_id'] = self.context['request'].user.id

        # Extraer datos de monitora si están presentes
        monitora_data = validated_data.pop('monitora', None)

        # Crear el Vehículo
        vehiculo = super().create(validated_data)

        # Crear la Monitora si hay datos
        if monitora_data:
            monitora_data['user_id'] = self.context['request'].user.id
            Monitora.objects.create(vehiculo=vehiculo, **monitora_data)

        return vehiculo

    #def update(self, instance, validated_data):
    #    """
    #    Se asegura de que la ruta existe antes de actualizar el vehículo.
    #    
    #        """
    #    monitora_data = validated_data.pop('monitora', None)
    #    validated_data['user_id'] = self.context['request'].user.id
    #    vehiculo = super().update(instance, validated_data)
    #    
    #    ruta_id = validated_data.get('ruta_id', instance.ruta_id)
    #    headers = self._get_auth_headers()
    #    response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
    #    if response.status_code != 200:
    #        raise ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')
#
    #    validated_data['user_id'] = self.context['request'].user.id
    #    monitora_data = validated_data.pop('monitora', None)
    #    if monitora_data:
    #        monitora = instance.monitora
    #        for attr, value in monitora_data.items():
    #            setattr(monitora, attr, value)
    #        monitora.user_id = self.context['request'].user.id
    #        monitora.save()
#
    #    return vehiculo
#

    def update(self, instance, validated_data):
        """
        Se asegura de que la ruta existe antes de actualizar el vehículo.
        """
        # Validar que la ruta existe antes de actualizar el vehículo
        ruta_id = validated_data.get('ruta_id', instance.ruta_id)
        headers = self._get_auth_headers()
        response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia de la ruta con ID {ruta_id}.')

        # Asignar user_id al validated_data
        validated_data['user_id'] = self.context['request'].user.id

        # Extraer datos de monitora si están presentes
        monitora_data = validated_data.pop('monitora', None)

        # Actualizar el Vehículo
        vehiculo = super().update(instance, validated_data)

        # Actualizar o crear la Monitora
        if monitora_data:
            monitora = getattr(instance, 'monitora', None)
            if monitora:
                # Actualizar monitora existente
                for attr, value in monitora_data.items():
                    setattr(monitora, attr, value)
                monitora.user_id = self.context['request'].user.id
                monitora.save()
            else:
                # Crear nueva monitora
                monitora_data['user_id'] = self.context['request'].user.id
                Monitora.objects.create(vehiculo=vehiculo, **monitora_data)

        return vehiculo
