# applications/api/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import DocumentoVehiculo
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_estado_documentos():
    documentos = DocumentoVehiculo.objects.all()
    vehiculos_actualizados = set()
    current_date = timezone.now().date()

    for documento in documentos:
        # Actualizar estado basado en fecha_expiracion
        if current_date > documento.fecha_expiracion and documento.estado != 'Vencido':
            documento.estado = 'Vencido'
            documento.save()
            vehiculos_actualizados.add(documento.vehiculo_id)
        elif current_date <= documento.fecha_expiracion and documento.estado != 'Vigente':
            documento.estado = 'Vigente'
            documento.save()
            vehiculos_actualizados.add(documento.vehiculo_id)

    # Actualizar rutas asociadas
    for vehiculo_id in vehiculos_actualizados:
        # Obtener documentos para el vehiculo
        documentos_vehiculo = DocumentoVehiculo.objects.filter(vehiculo_id=vehiculo_id)
        todos_vigentes = all(doc.estado == 'Vigente' for doc in documentos_vehiculo)

        # Obtener ruta_id del microservicio vehiculos
        headers = {
            'Authorization': f'Bearer {settings.SERVICE_TOKEN}',
            'Content-Type': 'application/json',
        }
        try:
            vehiculo_response = requests.get(
                f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/',
                headers=headers
            )
            vehiculo_response.raise_for_status()
            vehiculo_data = vehiculo_response.json()
            ruta_id = vehiculo_data.get('ruta_id')

            if ruta_id:
                # Actualizar el estado 'activa' en el microservicio rutas
                ruta_response = requests.patch(
                    f'http://rutas:8002/api/rutas/{ruta_id}/',
                    json={'activa': todos_vigentes},
                    headers=headers
                )
                ruta_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f'Error al actualizar ruta para vehiculo_id {vehiculo_id}: {e}')
