# models.py
from django.db import models
from datetime import timedelta, date

class DocumentoVehiculo(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('SOAT', 'SOAT'),
        ('Tecnomecanica', 'Tecnomecánica'),
        ('Poliza', 'Póliza')
    ]

    vehiculo_id = models.IntegerField('ID del Vehículo')  # Relación indirecta con Vehículo
    tipo_documento = models.CharField('Tipo de Documento', max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    fecha_expedicion = models.DateField('Fecha de Expedición')
    fecha_expiracion = models.DateField('Fecha de Expiración')
    estado = models.CharField('Estado del Documento', max_length=10, choices=[('Vigente', 'Vigente'), ('Vencido', 'Vencido')])
    vista_previa = models.FileField(upload_to='documentos/', null=True, blank=True)

    def __str__(self):
        return f"{self.tipo_documento} - Vehículo ID: {self.vehiculo_id}"

    class Meta:
        unique_together = ['vehiculo_id', 'tipo_documento']

    def save(self, *args, **kwargs):
        # Calcular fecha de expiración automáticamente para documentos con un año de vigencia
        if not self.fecha_expiracion:
            self.fecha_expiracion = self.fecha_expedicion + timedelta(days=365)
        # Verificar si el documento está vencido
        if date.today() > self.fecha_expiracion:
            self.estado = 'Vencido'
        else:
            self.estado = 'Vigente'
        super().save(*args, **kwargs)