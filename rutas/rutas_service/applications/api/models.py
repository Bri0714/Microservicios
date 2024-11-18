# models.py del servicio de rutas
from django.db import models

class Ruta(models.Model):
    ruta_nombre = models.CharField('Nombre de la Ruta', max_length=50)
    ruta_movil = models.IntegerField('Numero Movil')
    instituciones_ids = models.JSONField('IDs de Instituciones Asociadas', default=list)  # Relación a múltiples instituciones
    activa = models.BooleanField('Estado', default=True)
    
    # Nuevo campo para almacenar el ID del usuario
    user_id = models.IntegerField()
    
    class Meta:
        unique_together = ('user_id', 'ruta_movil', 'ruta_nombre')

    def __str__(self):
        return f"{self.ruta_nombre} - {self.ruta_movil}"

    