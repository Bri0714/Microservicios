# documentos_vehiculos/applications/api/tasks.py

from celery import shared_task
from .models import DocumentoVehiculo
from datetime import date
import requests
import logging
import os

# Configurar el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s: %(levelname)s/%(processName)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# documentos_vehiculos/applications/api/tasks.py

def get_service_token():
    """
    Obtiene un token JWT utilizando las credenciales de la cuenta de servicio.
    """
    auth_url = 'http://autenticacion:8000/api/login/'  # Usando el nombre del servicio en Docker Compose
    service_username = os.environ.get('SERVICE_EMAIL')  # Asegúrate de que SERVICE_EMAIL corresponde al 'username'
    service_password = os.environ.get('SERVICE_PASSWORD')

    if not service_username or not service_password:
        logger.error("SERVICE_EMAIL o SERVICE_PASSWORD no están configurados.")
        return None

    try:
        response = requests.post(
            auth_url,
            json={
                'username': service_username,  # Usar 'username' en lugar de 'email'
                'password': service_password
            },
            timeout=10
        )
        response.raise_for_status()
        token = response.json().get('token')
        if not token:
            logger.error("No se obtuvo el token en la respuesta.")
            return None
        return token
    except requests.RequestException as e:
        logger.error(f"Error al obtener el token de servicio: {e}")
        return None

@shared_task
def update_estado_documentos():
    # Obtener el token JWT
    token = get_service_token()
    
    if not token:
        logger.error("No se pudo obtener el token de servicio. Abortando tarea.")
        return
    
    # Headers con el token
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
    }
    
    # Obtener todos los documentos
    documentos = DocumentoVehiculo.objects.all()
    for documento in documentos:
        try:
            # Verificar si el documento ha expirado
            if documento.fecha_expiracion < date.today() and documento.estado != 'Vencido':
                documento.estado = 'Vencido'
                documento.save(update_fields=['estado'])
                logger.info(f"Documento {documento.id} actualizado a 'Vencido'")
            
            # Obtener el vehiculo_id
            vehiculo_id = documento.vehiculo_id
            if not vehiculo_id:
                logger.warning(f"Documento {documento.id} no tiene asociado un vehiculo_id.")
                continue
            
            # Obtener todos los documentos del vehículo
            documentos_vehiculo = DocumentoVehiculo.objects.filter(vehiculo_id=vehiculo_id)
            todos_vigentes = all(doc.estado == 'Vigente' for doc in documentos_vehiculo)
            logger.info(f"Vehículo {vehiculo_id} todos_vigentes: {todos_vigentes}")
    
            # Obtener el ruta_id asociado al vehiculo desde el servicio de vehiculos
            vehiculo_response = requests.get(
                f'http://vehiculos:8006/api/vehiculos/{vehiculo_id}/',
                headers=headers,
                timeout=20
            )
            if vehiculo_response.status_code == 200:
                vehiculo_data = vehiculo_response.json()
                ruta_id = vehiculo_data.get('ruta_id')
                if ruta_id:
                    # Actualizar el estado de la ruta
                    patch_response = requests.patch(
                        f'http://rutas:8002/api/rutas/{ruta_id}/',
                        json={'activa': todos_vigentes},
                        headers=headers,
                        timeout=20
                    )
                    if patch_response.status_code == 200:
                        logger.info(f"Ruta {ruta_id} actualizada a activa: {todos_vigentes}")
                    else:
                        logger.error(f"Error al actualizar ruta {ruta_id}: {patch_response.text}")
                else:
                    logger.warning(f"Vehículo {vehiculo_id} no tiene asociado un ruta_id.")
            else:
                logger.error(f"Error al obtener vehículo {vehiculo_id}: {vehiculo_response.text}")
        except Exception as e:
            logger.exception(f"Error procesando documento {documento.id}: {e}")
