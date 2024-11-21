# documentos_vehiculos/serializers.py

from rest_framework import serializers
from .models import DocumentoVehiculo
import requests
from django.core.exceptions import ValidationError
from datetime import timedelta, date

class DocumentoVehiculoSerializer(serializers.ModelSerializer):
    vehiculo = serializers.SerializerMethodField()  # Nuevo campo para mostrar la placa del vehículo asociado

    class Meta:
        model = DocumentoVehiculo
        fields = '__all__'
        read_only_fields = ['id', 'fecha_expiracion', 'estado']

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

    def validate_vista_previa(self, value):
        if value is not None and not value.name.endswith('.pdf'):
            raise serializers.ValidationError("El archivo de vista previa debe ser un archivo PDF.")
        return value

    def validate_vehiculo_id(self, value):
        """
        Valida que el vehículo con el ID proporcionado exista en el microservicio de vehículos.
        """
        headers = self._get_auth_headers()
        response = requests.get(f'http://vehiculos:8006/api/vehiculos/{value}/', headers=headers)
        if response.status_code != 200:
            raise ValidationError(f'El vehículo con ID {value} no existe o no se pudo verificar.')
        return value

    def validate(self, attrs):
            # Validar que la fecha de expiración sea posterior a la fecha de expedición
            if 'fecha_expedicion' in attrs:
                attrs['fecha_expiracion'] = attrs['fecha_expedicion'] + timedelta(days=365)
    
            # Verificar si se trata de una actualización
            instance = self.instance
            vehiculo_id = attrs.get('vehiculo_id', instance.vehiculo_id if instance else None)
            tipo_documento = attrs.get('tipo_documento', instance.tipo_documento if instance else None)
    
            # Validar unicidad del documento solo si se trata de una creación o si se está cambiando el tipo de documento
            if not instance or (instance and tipo_documento != instance.tipo_documento):
                if DocumentoVehiculo.objects.filter(vehiculo_id=vehiculo_id, tipo_documento=tipo_documento).exclude(id=instance.id if instance else None).exists():
                    raise serializers.ValidationError({
                        'tipo_documento': f'Ya existe un documento de tipo "{tipo_documento}" para el vehículo con ID {vehiculo_id}.'
                    })
    
            return attrs