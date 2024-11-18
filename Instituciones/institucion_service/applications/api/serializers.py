from rest_framework import serializers
from .models import Institucion

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'
        read_only_fields = ['id', 'user_id']

    def validate(self, attrs):
        user_id = self.context['request'].user.id
        institucion_contactos = attrs.get('institucion_contactos')
        institucion_telefono = attrs.get('institucion_telefono')

        # Obtener el ID de la institución actual si existe (en caso de actualización)
        institucion_id = self.instance.id if self.instance else None

        # Verificar unicidad del correo electrónico por usuario
        if Institucion.objects.filter(
            user_id=user_id,
            institucion_contactos=institucion_contactos
        ).exclude(id=institucion_id).exists():
            raise serializers.ValidationError({
                'institucion_contactos': 'Ya existe una institución con este correo electrónico para este usuario.'
            })

        # Verificar unicidad del teléfono por usuario
        if Institucion.objects.filter(
            user_id=user_id,
            institucion_telefono=institucion_telefono
        ).exclude(id=institucion_id).exists():
            raise serializers.ValidationError({
                'institucion_telefono': 'Ya existe una institución con este número de teléfono para este usuario.'
            })

        return attrs
