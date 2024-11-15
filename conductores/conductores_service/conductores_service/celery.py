from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.apps import apps
from django.conf import settings

# Establecer el módulo de configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conductores_service.settings.local')

# Crear la instancia de Celery
app = Celery('conductores_service')

# Cargar la configuración desde los ajustes de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodescubrimiento de tareas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
