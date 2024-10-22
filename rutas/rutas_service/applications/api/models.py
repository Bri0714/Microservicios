# models.py del servicio de rutas
from django.db import models

class Ruta(models.Model):
    ruta_nombre = models.CharField('Nombre de la Ruta', max_length=50, unique=True)
    ruta_movil = models.IntegerField('Numero Movil', unique=True)
    instituciones_ids = models.JSONField('IDs de Instituciones Asociadas', default=list)  # Relación a múltiples instituciones
    activa = models.BooleanField('Estado', default=True)

    def __str__(self):
        return f"{self.ruta_nombre} - {self.ruta_movil}"

    