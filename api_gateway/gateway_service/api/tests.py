from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from unittest.mock import patch
import requests

"""
- test_get_rutas_with_instituciones_success: Se asegura de que la API Gateway pueda obtener correctamente las rutas y sus instituciones.
- test_get_rutas_with_instituciones_connection_error: Verifica que la API maneje correctamente un error de conexión al servicio de rutas.
- test_get_rutas_with_instituciones_institucion_not_found: Prueba que el sistema maneje correctamente el caso en el que una institución no se encuentra.
- test_get_rutas_with_instituciones_timeout: Asegura que si el servicio de rutas tarda demasiado en responder, se maneje como un timeout.
"""

class APIGatewayTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.rutas_url = '/api/rutas_with_instituciones/'

    # Mock de una respuesta exitosa de rutas
    @patch('api.views.requests.get')
    def test_get_rutas_with_instituciones_success(self, mock_get):
        mock_rutas_response = {
            'id': 1,
            'ruta_nombre': 'Ruta 1',
            'ruta_movil': 5566,
            'institucion_id': 1
        }

        mock_institucion_response = {
            'id': 1,
            'institucion_nombre': 'Colegio A'
        }

        mock_get.side_effect = [
            MockResponse([mock_rutas_response], 200),
            MockResponse(mock_institucion_response, 200)
        ]

        response = self.client.get(self.rutas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['institucion']['id'], 1)
        self.assertEqual(response.data[0]['institucion']['institucion_nombre'], 'Colegio A')

    # Mock para una respuesta con error de conexión
    @patch('api.views.requests.get')
    def test_get_rutas_with_instituciones_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.ConnectionError

        response = self.client.get(self.rutas_url)
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)
        self.assertEqual(response.data['error'], 'Error de conexión al servicio de rutas')

    # Mock para simular que la institución no se encuentra
    @patch('api.views.requests.get')
    def test_get_rutas_with_instituciones_institucion_not_found(self, mock_get):
        mock_rutas_response = {
            'id': 1,
            'ruta_nombre': 'Ruta 1',
            'ruta_movil': 5566,
            'institucion_id': 1
        }

        mock_get.side_effect = [
            MockResponse([mock_rutas_response], 200),
            MockResponse({}, 404)
        ]

        response = self.client.get(self.rutas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data[0]['institucion'])

    # Mock para un timeout en la conexión
    @patch('api.views.requests.get')
    def test_get_rutas_with_instituciones_timeout(self, mock_get):
        mock_get.side_effect = requests.exceptions.Timeout

        response = self.client.get(self.rutas_url)
        self.assertEqual(response.status_code, status.HTTP_504_GATEWAY_TIMEOUT)
        self.assertEqual(response.data['error'], 'Tiempo de espera agotado al obtener rutas')


# Clase auxiliar para simular una respuesta de requests
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")
