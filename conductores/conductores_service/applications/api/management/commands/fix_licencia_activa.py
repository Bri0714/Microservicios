# conductores/applications/api/management/commands/fix_licencia_activa.py

from django.core.management.base import BaseCommand
from applications.api.models import Conductor
from datetime import date

class Command(BaseCommand):
    help = 'Corrige el campo licencia_activa basado en la fecha_expiracion'

    def handle(self, *args, **kwargs):
        conductores = Conductor.objects.all()
        updated = 0
        for conductor in conductores:
            original_status = conductor.licencia_activa
            if conductor.fecha_expiracion < date.today() and conductor.licencia_activa:
                conductor.licencia_activa = False
                conductor.save(update_fields=['licencia_activa'])
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Conductor {conductor} licencias desactivadas.'))
            elif conductor.fecha_expiracion >= date.today() and not conductor.licencia_activa:
                conductor.licencia_activa = True
                conductor.save(update_fields=['licencia_activa'])
                updated += 1
                self.stdout.write(self.style.SUCCESS(f'Conductor {conductor} licencias activadas.'))
        self.stdout.write(self.style.SUCCESS(f'Corrección de licencias completada. Total actualizaciones: {updated}'))
