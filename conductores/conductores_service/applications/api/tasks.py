# conductores/applications/api/tasks.py

from celery import shared_task
from .models import Conductor
from datetime import date

@shared_task
def update_licencia_activa():
    conductores = Conductor.objects.all()
    for conductor in conductores:
        # Verificar si la licencia ha expirado y está activa
        if conductor.fecha_expiracion < date.today() and conductor.licencia_activa:
            conductor.licencia_activa = False
            conductor.save(update_fields=['licencia_activa'])
        
        # Verificar si la licencia no ha expirado y está inactiva
        elif conductor.fecha_expiracion >= date.today() and not conductor.licencia_activa:
            conductor.licencia_activa = True
            conductor.save(update_fields=['licencia_activa'])
