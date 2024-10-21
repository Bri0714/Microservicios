# models.py
from django.db import models

class Acudiente(models.Model):
    acudiente_nombre = models.CharField(max_length=100, null=False, blank=False)
    acudiente_apellido = models.CharField(max_length=200, null=False, blank=False)
    PARENTESCO_CHOICES = [
        ('Padre', 'Padre'),
        ('Madre', 'Madre'),
        ('Tio', 'Tio'),
        ('Abuelo', 'Abuelo'),
        ('Otro', 'Otro')
    ]
    acudiente_parentesco = models.CharField(max_length=50, choices=PARENTESCO_CHOICES, null=False, blank=False)
    acudiente_telefono = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return f"{self.acudiente_nombre} {self.acudiente_apellido}"

class Estudiante(models.Model):
    
    acudiente = models.ForeignKey(Acudiente, on_delete=models.CASCADE, related_name='estudiantes')
    colegio_id = models.IntegerField(null=False, blank=False)  # Relación con la institución (ID externo)
    ruta_id = models.IntegerField(null=False, blank=False)  # Relación con la ruta (ID externo)
    #estudiante foto 
    estudiante_foto = models.ImageField(upload_to='logos/', null=True, blank=True)
    estudiante_nombre = models.CharField(max_length=100, null=False, blank=False)
    estudiante_apellido = models.CharField(max_length=100, null=False, blank=False)
    estudiante_edad = models.PositiveIntegerField(null=False, blank=False)
    estudiante_curso = models.CharField(max_length=50, null=False, blank=False)
    estudiante_direccion = models.CharField(max_length=255, null=False, blank=False)  

    def __str__(self):
        return f"{self.estudiante_nombre} {self.estudiante_apellido}"
