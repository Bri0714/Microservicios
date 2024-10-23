from rest_framework import serializers
from .models import Conductor

class Conductorserializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = '__all__'
        
    def validate_fecha_expiracion(self, value):
        # Validar que la fecha de expiración sea posterior a la fecha de expedición
        if value <= self.instance.fecha_exp:
            raise serializers.ValidationError('La fecha de expiración debe ser posterior a la fecha de expedición de la licencia.')
        return value