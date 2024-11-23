from rest_framework import serializers
from .models import Pago
import requests
from rest_framework.serializers import ValidationError
from decimal import Decimal
from datetime import datetime
import calendar
from django.utils import timezone

class EstudianteDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    estudiante_foto = serializers.ImageField()
    estudiante_nombre = serializers.CharField(max_length=100)
    estudiante_apellido = serializers.CharField(max_length=100)
    estudiante_edad = serializers.IntegerField()
    estudiante_curso = serializers.CharField(max_length=50)
    estudiante_direccion = serializers.CharField(max_length=255)
    pago_ruta = serializers.DecimalField(max_digits=12, decimal_places=2)
    estudiante_fecha_ingreso_ruta = serializers.DateField()
    estudiante_estado = serializers.BooleanField()

class PagoSerializer(serializers.ModelSerializer):
    estudiante = EstudianteDataSerializer(read_only=True)
    user_id = serializers.IntegerField(read_only=True)
    estado_pago = serializers.BooleanField(read_only=True)
    pago_multas = serializers.BooleanField(required=False, allow_null=True)

    class Meta:
        model = Pago
        fields = [
            'id',
            'numero_talonario',
            'mes_a_pagar',
            'fecha_de_pago',
            'fecha_vencimiento_pago',
            'multas',
            'estudiante_id',
            'user_id',
            'estado_pago',
            'pago_multas',
            'estudiante',
        ]
        read_only_fields = ['id', 'fecha_vencimiento_pago', 'multas', 'user_id', 'estado_pago', 'estudiante']

    def validate_numero_talonario(self, value):
        if not value.isdigit() or len(value) not in [5, 6]:
            raise serializers.ValidationError('El número de talonario debe tener 5 o 6 dígitos numéricos.')
        return value

    def validate_mes_a_pagar(self, value):
        valid_months = [choice[0] for choice in Pago.MES_CHOICES]
        if value not in valid_months:
            raise serializers.ValidationError(f'El mes a pagar debe ser uno de los siguientes: {", ".join(valid_months)}.')
        return value

    def validate_estudiante_id(self, value):
        # Validar que el estudiante existe en el microservicio de Estudiantes
        estudiante_data = self.get_estudiante_data(value)
        if not estudiante_data:
            raise serializers.ValidationError(f'El estudiante con ID {value} no existe.')
        return value

    def validate(self, data):
        user_id = self.context['request'].user.id
        estudiante_id = data.get('estudiante_id', getattr(self.instance, 'estudiante_id', None))
        mes_a_pagar = data.get('mes_a_pagar', getattr(self.instance, 'mes_a_pagar', None))
        numero_talonario = data.get('numero_talonario', getattr(self.instance, 'numero_talonario', None))

        # Obtener la instancia actual si se está actualizando
        instance = self.instance

        # Validar que numero_talonario es único globalmente
        if Pago.objects.filter(
            numero_talonario=numero_talonario
        ).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError({'numero_talonario': 'El número de talonario ya está en uso.'})

        # Validar que no haya más de un pago por estudiante en el mismo mes
        if Pago.objects.filter(
            user_id=user_id,
            estudiante_id=estudiante_id,
            mes_a_pagar=mes_a_pagar
        ).exclude(id=instance.id if instance else None).exists():
            raise serializers.ValidationError({'mes_a_pagar': 'Ya existe un pago registrado para este mes y estudiante.'})

        return data

    def get_estudiante_data(self, estudiante_id):
        try:
            request = self.context.get('request')
            auth_header = request.headers.get('Authorization') if request else None

            response = requests.get(
                f'http://estudiantes:8004/api/estudiantes/{estudiante_id}/',
                headers={'Authorization': auth_header} if auth_header else {},
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
            return None
        except requests.exceptions.RequestException:
            return None

    def calculate_fecha_vencimiento(self, fecha_ingreso, mes_a_pagar):
        """
        Calcula la fecha de vencimiento basada en el mes a pagar y la fecha de ingreso.
        """
        mes_map = {
            "Enero": 1,
            "Febrero": 2,
            "Marzo": 3,
            "Abril": 4,
            "Mayo": 5,
            "Junio": 6,
            "Julio": 7,
            "Agosto": 8,
            "Septiembre": 9,
            "Octubre": 10,
            "Noviembre": 11,
            "Diciembre": 12
        }

        mes_num = mes_map.get(mes_a_pagar)
        if not mes_num:
            raise ValidationError(f"Mes a pagar inválido: {mes_a_pagar}")

        fecha_ingreso_date = datetime.strptime(fecha_ingreso, '%Y-%m-%d').date()
        year = fecha_ingreso_date.year

        # Ajustar el año si el mes a pagar es menor que el mes de ingreso
        if mes_num < fecha_ingreso_date.month:
            year += 1

        try:
            fecha_vencimiento = fecha_ingreso_date.replace(month=mes_num, year=year)
        except ValueError:
            # Manejar casos como 30 de febrero
            last_day = calendar.monthrange(year, mes_num)[1]
            fecha_vencimiento = fecha_ingreso_date.replace(day=last_day, month=mes_num, year=year)

        return fecha_vencimiento

    def calculate_multas(self, fecha_vencimiento_pago, fecha_de_pago=None):
        today = timezone.now().date()
        if fecha_de_pago:
            # Si se realizó el pago, calcular multas basadas en la fecha de pago
            if fecha_de_pago > fecha_vencimiento_pago:
                delta = fecha_de_pago - fecha_vencimiento_pago
                semanas = delta.days // 7
                return Decimal(semanas * 10000)
            else:
                return Decimal('0.00')
        else:
            # Si no se realizó el pago, calcular multas hasta hoy
            if today > fecha_vencimiento_pago:
                delta = today - fecha_vencimiento_pago
                semanas = delta.days // 7
                return Decimal(semanas * 10000)
            else:
                return Decimal('0.00')

    def create(self, validated_data):
        estudiante_id = validated_data.get('estudiante_id')
        mes_a_pagar = validated_data.get('mes_a_pagar')
        estudiante_data = self.get_estudiante_data(estudiante_id)
        if not estudiante_data:
            raise serializers.ValidationError('El estudiante no existe o no está disponible.')

        # Calcular fecha_vencimiento_pago basado en mes_a_pagar
        estudiante_fecha_ingreso_ruta = estudiante_data.get('estudiante_fecha_ingreso_ruta')
        fecha_vencimiento_pago = self.calculate_fecha_vencimiento(estudiante_fecha_ingreso_ruta, mes_a_pagar)
        validated_data['fecha_vencimiento_pago'] = fecha_vencimiento_pago

        # Asignar user_id desde el contexto
        request = self.context.get('request')
        if request and hasattr(request.user, 'id'):
            validated_data['user_id'] = request.user.id
        else:
            raise serializers.ValidationError('No se pudo obtener el usuario autenticado.')

        # Obtener fecha_de_pago si está presente
        fecha_de_pago = validated_data.get('fecha_de_pago')

        # Calcular multas
        multas = self.calculate_multas(fecha_vencimiento_pago, fecha_de_pago)
        validated_data['multas'] = multas

        # Inicializar estado_pago como False
        estado_pago = False

        # Verificar si hay fecha_de_pago y actualizar estado_pago
        if fecha_de_pago:
            if fecha_de_pago <= fecha_vencimiento_pago:
                estado_pago = True
            elif validated_data.get('pago_multas') is True:
                estado_pago = True
        else:
            # Si no hay fecha_de_pago, determinar estado_pago basado en la fecha actual
            if fecha_vencimiento_pago >= timezone.now().date():
                estado_pago = True

        validated_data['estado_pago'] = estado_pago

        # Manejar pago_multas
        pago_multas = validated_data.get('pago_multas', None)
        if pago_multas is True:
            estado_pago = True
            validated_data['estado_pago'] = estado_pago
            validated_data['multas'] = Decimal('0.00')  # Establecer multas a cero

        # Crear el Pago
        pago = Pago.objects.create(**validated_data)

        return pago

    def update(self, instance, validated_data):
        # Actualizar campos
        instance.numero_talonario = validated_data.get('numero_talonario', instance.numero_talonario)
        instance.mes_a_pagar = validated_data.get('mes_a_pagar', instance.mes_a_pagar)
        instance.estudiante_id = validated_data.get('estudiante_id', instance.estudiante_id)

        # Si estudiante_id o mes_a_pagar cambian, recalcular fecha_vencimiento_pago y multas
        if 'estudiante_id' in validated_data or 'mes_a_pagar' in validated_data:
            estudiante_data = self.get_estudiante_data(instance.estudiante_id)
            if not estudiante_data:
                raise serializers.ValidationError('El estudiante no existe o no está disponible.')

            estudiante_fecha_ingreso_ruta = estudiante_data.get('estudiante_fecha_ingreso_ruta')
            fecha_vencimiento_pago = self.calculate_fecha_vencimiento(estudiante_fecha_ingreso_ruta, instance.mes_a_pagar)
            instance.fecha_vencimiento_pago = fecha_vencimiento_pago

            # Recalcular multas
            instance.multas = self.calculate_multas(fecha_vencimiento_pago, instance.fecha_de_pago)

            # Recalcular estado_pago basado en la nueva fecha_vencimiento_pago y estado actual
            if fecha_vencimiento_pago >= timezone.now().date():
                instance.estado_pago = True
            else:
                if instance.pago_multas:
                    instance.estado_pago = True
                elif instance.fecha_de_pago and instance.fecha_de_pago <= fecha_vencimiento_pago:
                    instance.estado_pago = True
                else:
                    instance.estado_pago = False

        # Manejar pago_multas
        if 'pago_multas' in validated_data:
            pago_multas = validated_data.get('pago_multas')
            instance.pago_multas = pago_multas
            if pago_multas is True:
                instance.estado_pago = True
                instance.multas = Decimal('0.00')  # Establecer multas a cero

        # Manejar fecha_de_pago
        if 'fecha_de_pago' in validated_data:
            instance.fecha_de_pago = validated_data['fecha_de_pago']
            if not instance.pago_multas:
                # Recalcular multas solo si pago_multas no es True
                instance.multas = self.calculate_multas(instance.fecha_vencimiento_pago, instance.fecha_de_pago)
            else:
                # Establecer multas a cero si pago_multas es True
                instance.multas = Decimal('0.00')

            # Actualizar estado_pago basado en la lógica
            if instance.fecha_de_pago <= instance.fecha_vencimiento_pago:
                instance.estado_pago = True
            elif instance.pago_multas:
                instance.estado_pago = True
            else:
                instance.estado_pago = False

        instance.save()

        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        estudiante_data = self.get_estudiante_data(instance.estudiante_id)
        if estudiante_data:
            representation['estudiante'] = {
                'estudiante_id': estudiante_data.get('id'),
                'estudiante_foto': estudiante_data.get('estudiante_foto'),
                'estudiante_nombre': estudiante_data.get('estudiante_nombre'),
                'estudiante_apellido': estudiante_data.get('estudiante_apellido'),
                'estudiante_edad': estudiante_data.get('estudiante_edad'),
                'estudiante_curso': estudiante_data.get('estudiante_curso'),
                'estudiante_direccion': estudiante_data.get('estudiante_direccion'),
                'pago_ruta': str(estudiante_data.get('pago_ruta')),
                'estudiante_fecha_ingreso_ruta': estudiante_data.get('estudiante_fecha_ingreso_ruta'),
                'estudiante_estado': estudiante_data.get('estudiante_estado'),
            }
        else:
            representation['estudiante'] = None
        return representation