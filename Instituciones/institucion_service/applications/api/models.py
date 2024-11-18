from django.db import models

class Institucion(models.Model):
    # Campos existentes
    institucion_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    institucion_nombre = models.CharField('Nombre', max_length=50)
    institucion_direccion = models.CharField('Direccion', max_length=50)
    institucion_nit = models.CharField('Nit', max_length=20)
    institucion_contactos = models.EmailField('Correo Electronico', max_length=254)
    institucion_telefono = models.CharField('Telefono', max_length=50)

    # Nuevo campo para almacenar el ID del usuario
    user_id = models.IntegerField()
    
    class Meta:
        unique_together = ('user_id', 'institucion_telefono', 'institucion_contactos')

    def __str__(self):
        return f"{self.institucion_nombre}, {self.institucion_nit}"
