from rest_framework import serializers
from .models import Institucion

class InstitucionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institucion
        fields = '__all__'
        read_only_fields = ['id', 'user_id']
