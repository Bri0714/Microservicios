# conductores/applications/api/management/commands/correct_edades.py

from django.core.management.base import BaseCommand
from applications.api.models import Conductor
from rest_framework.exceptions import ValidationError

class Command(BaseCommand):
    help = 'Corrige edades inválidas de los conductores'

    def handle(self, *args, **kwargs):
        conductores = Conductor.objects.all()
        invalid_ages = 0
        for conductor in conductores:
            if conductor.edad < 18 or conductor.edad > 120:
                self.stdout.write(self.style.WARNING(f'Conductor {conductor} tiene edad inválida: {conductor.edad}.'))
                # Opcional: Actualizar a una edad válida o eliminar el registro
                # Por ejemplo, puedes eliminar el registro:
                # conductor.delete()
                invalid_ages += 1
        self.stdout.write(self.style.SUCCESS(f'Corrección de edades completada. Total edades inválidas encontradas: {invalid_ages}'))
