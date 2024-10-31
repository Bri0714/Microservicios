#from django.db import models
#
## Create your models here.
#
## Creacion del modelo del microservicio instituciones
#
#class Institucion(models.Model):
#    # django se encarga de asignarle un id a la entidad institucion 
#    # logo del colegio 
#    institucion_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
#    institucion_nombre = models.CharField('Nombre', max_length=50)
#    institucion_direccion = models.CharField('Direccion', max_length=50)
#    institucion_nit = models.CharField('Nit', max_length=20)
#    institucion_contactos = models.EmailField('Correo Electronico', max_length=254, unique=True)
#    institucion_telefono = models.CharField('Telefono', max_length=50, unique=True)
#
#    def __str__(self):
#        return f"{self.institucion_nombre},{self.institucion_nit}"

# instituciones/models.py

from django.db import models

class Institucion(models.Model):
    # Campos existentes
    institucion_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    institucion_nombre = models.CharField('Nombre', max_length=50)
    institucion_direccion = models.CharField('Direccion', max_length=50)
    institucion_nit = models.CharField('Nit', max_length=20)
    institucion_contactos = models.EmailField('Correo Electronico', max_length=254, unique=True)
    institucion_telefono = models.CharField('Telefono', max_length=50, unique=True)

    # Nuevo campo para almacenar el ID del usuario
    user_id = models.IntegerField()

    def __str__(self):
        return f"{self.institucion_nombre}, {self.institucion_nit}"
