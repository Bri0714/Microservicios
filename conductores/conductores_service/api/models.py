# models.py del servicio de conductores
from django.db import models
from datetime import date

class Conductor(models.Model):
    nombre = models.CharField('Nombre del Conductor', max_length=50)
    apellido = models.CharField('Apellido del Conductor', max_length=50)
    edad = models.IntegerField('Edad del Conductor')
    telefono = models.CharField('Teléfono del Conductor', max_length=15)
    foto = models.ImageField('Foto del Conductor', upload_to='logos/')
    fecha_exp = models.DateField('Fecha de Expedición de Licencia')
    fecha_expiracion = models.DateField('Fecha de Expiración de Licencia')
    licencia_activa = models.BooleanField('Licencia Activa', default=True)

    def save(self, *args, **kwargs):
        # Verificar si la licencia ha expirado y actualizar el campo licencia_activa
        if self.fecha_expiracion < date.today():
            self.licencia_activa = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"