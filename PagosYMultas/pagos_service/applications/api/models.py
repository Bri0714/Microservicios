# applications/api/models.py

from django.db import models

class Pago(models.Model):
    MES_CHOICES = [
        ('Febrero', 'Febrero'),
        ('Marzo', 'Marzo'),
        ('Abril', 'Abril'),
        ('Mayo', 'Mayo'),
        ('Junio', 'Junio'),
        ('Julio', 'Julio'),
        ('Agosto', 'Agosto'),
        ('Septiembre', 'Septiembre'),
        ('Octubre', 'Octubre'),
        ('Noviembre', 'Noviembre'),
    ]

    numero_talonario = models.CharField(max_length=6)
    mes_a_pagar = models.CharField(max_length=10, choices=MES_CHOICES)
    fecha_de_pago = models.DateField(null=True, blank=True)  # Puede ser null si aún no se ha pagado
    fecha_vencimiento_pago = models.DateField(editable=False)
    multas = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, editable=False)
    estudiante_id = models.IntegerField()
    user_id = models.IntegerField(editable=False)  # Relación con el usuario que realiza el pago
    estado_pago = models.BooleanField(default=False)
    pago_multas = models.BooleanField(null=True, blank=True)

    #class Meta:
    #    unique_together = (
    #        ('user_id', 'numero_talonario'),
    #        ('estudiante_id', 'mes_a_pagar'),
    #    )

    def __str__(self):
        return f'Pago {self.numero_talonario} - Estudiante ID {self.estudiante_id}'
