from django.db import models

# Create your models here.
class Pago(models.Model):
    id_pago = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField()
    id_multa = models.ForeignKey('Multa', models.DO_NOTHING, db_column='id_multa')

