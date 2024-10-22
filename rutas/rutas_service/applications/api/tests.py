from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from unittest.mock import patch
from .models import Ruta

class RutaTests(APITestCase):
    @patch('applications.api.serializers.requests.get')
    def setUp(self, mock_get):
        # Simular las respuestas del servicio de Instituciones
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.side_effect = [
            {
                "id": 1,
                "institucion_nombre": "Instituto Infantil Y Juvenil",
                "institucion_direccion": "Cll. 22a # 96i-06",
                "institucion_nit": "901.316.552",
                "institucion_contactos": "secretaria@injuv.edu.co",
                "institucion_telefono": "+57 601 2671208"
            },
            {
                "id": 2,
                "institucion_nombre": "Villermar El carmen",
                "institucion_direccion": "Cra 96g no 33-45",
                "institucion_nit": "99.22.55.66",
                "institucion_contactos": "villermar_el_carmen@hotmail.com",
                "institucion_telefono": "+57 601 2335566"
            }
        ]
        # Crear ruta asociada a ambas instituciones
        self.ruta = Ruta.objects.create(
            ruta_nombre="Ruta 1",
            ruta_movil=6633,
            instituciones_ids=[1, 2],
            activa=True
        )

    @patch('applications.api.serializers.requests.get')
    def test_create_ruta(self, mock_get):
        """Prueba la creación de una ruta."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "institucion_nombre": "Instituto Infantil Y Juvenil"
        }
        url = reverse('ruta_app:ruta-list')
        response = self.client.post(url, {
            "ruta_nombre": "Ruta 2",
            "ruta_movil": 6789,
            "instituciones_ids": [1, 2],
            "activa": True
        }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ruta.objects.count(), 2)
        self.assertEqual(Ruta.objects.get(ruta_nombre="Ruta 2").ruta_nombre, "Ruta 2")

    @patch('applications.api.serializers.requests.get')
    def test_get_ruta(self, mock_get):
        """Prueba la obtención de una ruta existente."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "institucion_nombre": "Instituto Infantil Y Juvenil"
        }
        url = reverse('ruta_app:ruta-detail', args=[self.ruta.id])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ruta_nombre'], self.ruta.ruta_nombre)
        self.assertEqual(len(response.data['instituciones']), 2)

    @patch('applications.api.serializers.requests.get')
    def test_create_ruta_invalid_institucion(self, mock_get):
        """Prueba que no se pueda crear una ruta con una institución inválida."""
        mock_get.return_value.status_code = 404

        invalid_ruta_data = {
            "ruta_nombre": "Ruta Invalida",
            "ruta_movil": 9876,
            "instituciones_ids": [999],  # ID de institución no existente
            "activa": True
        }

        url = reverse('ruta_app:ruta-list')
        response = self.client.post(url, invalid_ruta_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('instituciones_ids', response.data)

    @patch('applications.api.serializers.requests.get')
    def test_update_ruta(self, mock_get):
        """Prueba la actualización de una ruta existente."""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "id": 1,
            "institucion_nombre": "Instituto Infantil Y Juvenil"
        }
        updated_ruta_data = {
            "ruta_nombre": "Ruta 1 Actualizada",
            "ruta_movil": 6634,
            "instituciones_ids": [1],
            "activa": False
        }
        url = reverse('ruta_app:ruta-detail', args=[self.ruta.id])
        response = self.client.put(url, updated_ruta_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ruta.refresh_from_db()
        self.assertEqual(self.ruta.ruta_nombre, updated_ruta_data['ruta_nombre'])
        self.assertEqual(self.ruta.ruta_movil, updated_ruta_data['ruta_movil'])
        self.assertFalse(self.ruta.activa)
        self.assertEqual(len(self.ruta.instituciones_ids), 1)

    @patch('applications.api.serializers.requests.get')
    def test_delete_ruta(self, mock_get):
        """Prueba la eliminación de una ruta existente."""
        mock_get.return_value.status_code = 200
        url = reverse('ruta_app:ruta-detail', args=[self.ruta.id])
        response = self.client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ruta.objects.count(), 0)