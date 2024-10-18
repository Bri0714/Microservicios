from django.db import models

# Create your models here.
class Ruta(models.Model):
    ruta_nombre = models.CharField('Nombre de la Ruta', max_length=50,unique=True)
    ruta_movil = models.IntegerField('Numero Movil',unique=True)
    institucion_id = models.IntegerField('ID de institucion',null=False)
    activa = models.BooleanField('Estado',default=True)

    def __str__(self):
        return f"{self.ruta_nombre} - {self.ruta_movil}"
    