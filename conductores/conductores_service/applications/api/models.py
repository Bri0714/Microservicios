# models.py del servicio de conductores
from django.db import models
from datetime import date, timedelta

class Conductor(models.Model):
    nombre = models.CharField('Nombre del Conductor', max_length=50)
    apellido = models.CharField('Apellido del Conductor', max_length=50)
    edad = models.IntegerField('Edad del Conductor')
    telefono = models.CharField('Teléfono del Conductor', max_length=15, unique=True)
    foto = models.ImageField('Foto del Conductor', upload_to='conductores_fotos/', null=True)
    fecha_exp = models.DateField('Fecha de Expedición de Licencia')
    fecha_expiracion = models.DateField('Fecha de Expiración de Licencia', blank=True, null=True)
    licencia_activa = models.BooleanField('Licencia Activa', default=True)
    vehiculo_id = models.IntegerField('ID del Vehículo', unique=True)  # Relación con Vehículo (relación uno a uno)
    
    user_id = models.IntegerField()  # Campo para almacenar el ID del usuario

    def save(self, *args, **kwargs):
        # Asignar la fecha de expiración automáticamente según la edad del conductor
        if not self.fecha_expiracion:
            if self.edad < 60:
                self.fecha_expiracion = self.fecha_exp + timedelta(days=3*365)
            elif self.edad > 60:
                self.fecha_expiracion = self.fecha_exp + timedelta(days=1*365)
        
        # Verificar si la licencia ha expirado y actualizar el campo licencia_activa
        if self.fecha_expiracion < date.today():
            self.licencia_activa = False
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"