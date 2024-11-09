from django.db import models

class Vehiculo(models.Model):
    vehiculo_placa = models.CharField('Placa del Vehículo', max_length=10, unique=True)
    vehiculo_marca = models.CharField('Marca del Vehículo', max_length=50)
    vehiculo_modelo = models.IntegerField('Modelo del Vehículo')
    vehiculo_imagen = models.ImageField(upload_to='vehiculos/', null=True, blank=True)
    vehiculo_capacidad = models.PositiveIntegerField('Capacidad del Vehículo')
    ruta_id = models.IntegerField('ID de la Ruta', unique=True)  # Relación con Ruta (relación uno a uno)
    user_id = models.IntegerField()  # Campo para almacenar el ID del usuario

    def __str__(self):
        return f"{self.vehiculo_placa} - {self.vehiculo_marca}"

class Monitora(models.Model):
    nombre_completo = models.CharField('Nombre Completo', max_length=100)
    edad = models.PositiveIntegerField('Edad')
    telefono = models.CharField('Teléfono', max_length=10 , unique=True)
    vehiculo = models.OneToOneField(Vehiculo, on_delete=models.CASCADE, related_name='monitora')  # Relación con Vehículo (relación uno a uno)
    user_id = models.IntegerField()  # Campo para almacenar el ID del usuario

    def __str__(self):
        return f"{self.nombre_completo} - {self.telefono}"
