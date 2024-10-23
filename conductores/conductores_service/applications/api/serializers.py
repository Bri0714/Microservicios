# serializers.py del servicio de conductores
from rest_framework import serializers
from .models import Conductor
from datetime import timedelta

class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'

    def validate_edad(self, value):
        # Validar que la edad sea mayor a 18 años
        if value < 18:
            raise serializers.ValidationError('La edad del conductor debe ser mayor a 18 años.')
        return value

    def validate(self, data):
        # Calcular automáticamente la fecha de expiración según la edad del conductor y la fecha de expedición
        if 'fecha_exp' in data:
            edad = data.get('edad')
            fecha_exp = data['fecha_exp']
            if edad < 60:
                data['fecha_expiracion'] = fecha_exp + timedelta(days=3*365)
            elif edad > 60:
                data['fecha_expiracion'] = fecha_exp + timedelta(days=1*365)
        return data

