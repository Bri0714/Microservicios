# serializers.py del servicio de conductores
from rest_framework import serializers
from .models import Conductor
from datetime import timedelta
import requests
from rest_framework.exceptions import ValidationError


class ConductorSerializer(serializers.ModelSerializer):
    vehiculo = serializers.SerializerMethodField()  # Devuelve la placa del vehículo relacionado
    
    class Meta:
        model = Conductor
        fields = '__all__'
        read_only_fields = ['id', 'user_id', 'fecha_expiracion', 'licencia_activa']

    def _get_auth_headers(self):
        """
        Obtiene el token JWT del request context y lo agrega en el encabezado de autorización.
        """
        request = self.context.get('request')
        token = request.headers.get('Authorization') if request else None
        if not token:
            raise ValidationError('No se pudo obtener el token de autorización.')
        return {'Authorization': token}

    def get_vehiculo(self, obj):
        """
        Obtiene la placa del vehículo relacionado utilizando vehiculo_id.
        """
        if obj.vehiculo_id:
            headers = self._get_auth_headers()
            response = requests.get(f'http://vehiculos:8006/api/vehiculos/{obj.vehiculo_id}/', headers=headers)
            if response.status_code == 200:
                vehiculo_data = response.json()
                return vehiculo_data.get('vehiculo_placa', 'Información no disponible')
        return 'Información no disponible'
    
    def validate(self, attrs):
        user_id = self.context['request'].user.id
        telefono = attrs.get('telefono')
        vehiculo_id = attrs.get('vehiculo_id')

        conductor_id = self.instance.id if self.instance else None

        # Verificar unicidad de telefono por usuario
        if Conductor.objects.filter(
            user_id=user_id,
            telefono=telefono
        ).exclude(id=conductor_id).exists():
            raise serializers.ValidationError({
                'telefono': 'Ya existe un conductor con este teléfono para este usuario.'
            })

        # Verificar unicidad de vehiculo_id por usuario
        if Conductor.objects.filter(
            user_id=user_id,
            vehiculo_id=vehiculo_id
        ).exclude(id=conductor_id).exists():
            raise serializers.ValidationError({
                'vehiculo_id': 'Ya existe un conductor asociado a este vehículo para este usuario.'
            })

        # Validar que el vehículo existe en el microservicio
        headers = self._get_auth_headers()
        response = requests.get(f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers)
        if response.status_code != 200:
            raise serializers.ValidationError({
                'vehiculo_id': f'El vehículo con ID {vehiculo_id} no existe o no se pudo verificar.'
            })

        # Calcular automáticamente la fecha de expiración según la edad del conductor y la fecha de expedición
        edad = attrs.get('edad')
        fecha_exp = attrs.get('fecha_exp')
        if edad and fecha_exp:
            if edad < 60:
                attrs['fecha_expiracion'] = fecha_exp + timedelta(days=3*365)
            else:
                attrs['fecha_expiracion'] = fecha_exp + timedelta(days=1*365)

        return attrs


    def validate_edad(self, value):
        # Validar que la edad sea mayor a 18 años
        if value < 18:
            raise serializers.ValidationError('La edad del conductor debe ser mayor a 18 años.')
        return value

    def validate_vehiculo_id(self, value):
        """
        Valida que el vehículo con el ID proporcionado exista.
        """
        headers = self._get_auth_headers()
        response = requests.get(f'http://vehiculos:8006/api/vehiculos/{value}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'El vehículo con ID {value} no existe o no se pudo verificar.')
        return value

    def validate(self, data):
        # Calcular automáticamente la fecha de expiración según la edad del conductor y la fecha de expedición
        if 'fecha_exp' in data:
            edad = data.get('edad')
            fecha_exp = data['fecha_exp']
            if edad < 60:
                data['fecha_expiracion'] = fecha_exp + timedelta(days=3*365)
            elif edad >= 60:
                data['fecha_expiracion'] = fecha_exp + timedelta(days=1*365)
        return data

    def create(self, validated_data):
        """
        Se asegura de que el vehículo existe antes de crear el conductor.
        """
        validated_data['user_id'] = self.context['request'].user.id
        vehiculo_id = validated_data.get('vehiculo_id')
        headers = self._get_auth_headers()
        response = requests.get(f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia del vehículo con ID {vehiculo_id}.')

        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Se asegura de que el vehículo existe antes de actualizar el conductor.
        """
        validated_data['user_id'] = self.context['request'].user.id
        vehiculo_id = validated_data.get('vehiculo_id', instance.vehiculo_id)
        headers = self._get_auth_headers()
        response = requests.get(f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'No se pudo verificar la existencia del vehículo con ID {vehiculo_id}.')

        return super().update(instance, validated_data)
