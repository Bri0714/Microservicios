from django.test import TestCase
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
import requests

class APIGatewayTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch('requests.get')
    def test_get_rutas_with_instituciones_success(self, mock_get):
        # Mocking institution and route responses
        mock_get.side_effect = [
            # First call returns the institution data
            MockResponse({"id": 1, "institucion_nombre": "Institucion 1"}, 200),
            # Second call returns associated routes
            MockResponse([{"id": 1, "instituciones_ids": [1], "ruta_nombre": "Ruta 1", "ruta_movil": "1234", "activa": True}], 200)
        ]
        
        response = self.client.get('/api/instituciones/1/rutas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('rutas', response.json())

    @patch('requests.get')
    def test_get_rutas_with_instituciones_institucion_not_found(self, mock_get):
        # Mocking institution response as 404
        mock_get.side_effect = [
            MockResponse({"error": "La institución con el ID proporcionado no existe."}, 404)
        ]
        
        response = self.client.get('/api/instituciones/99/rutas/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], "La institución con el ID proporcionado no existe.")

    @patch('requests.get')
    def test_get_rutas_with_instituciones_timeout(self, mock_get):
        # Simulate timeout for institution service
        mock_get.side_effect = requests.exceptions.Timeout()
        
        response = self.client.get('/api/instituciones/1/rutas/')
        self.assertEqual(response.status_code, status.HTTP_504_GATEWAY_TIMEOUT)

    @patch('requests.get')
    def test_get_rutas_with_instituciones_connection_error(self, mock_get):
        # Simulate connection error for institution service
        mock_get.side_effect = requests.exceptions.ConnectionError()
        
        response = self.client.get('/api/instituciones/1/rutas/')
        self.assertEqual(response.status_code, status.HTTP_503_SERVICE_UNAVAILABLE)

    @patch('requests.get')
    def test_get_estudiantes_por_institucion_y_ruta_success(self, mock_get):
        # Mocking institution, route, and students data
        mock_get.side_effect = [
            # First call returns the institution data
            MockResponse({"id": 1, "institucion_nombre": "Institucion 1"}, 200),
            # Second call returns the route data
            MockResponse({"id": 1, "instituciones_ids": [1], "ruta_nombre": "Ruta 1"}, 200),
            # Third call returns students data
            MockResponse([{"id": 1, "colegio_id": 1, "ruta_id": 1, "estudiante_nombre": "Juan", "estudiante_apellido": "Perez", "estudiante_edad": 10}], 200)
        ]
        
        response = self.client.get('/api/instituciones/1/rutas/1/estudiantes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['estudiantes']), 1)

    @patch('requests.get')
    def test_get_estudiantes_por_institucion_y_ruta_institucion_not_found(self, mock_get):
        # Mocking institution response as 404
        mock_get.side_effect = [
            MockResponse({"error": "La institución con ID 99 no existe."}, 404)
        ]
        
        response = self.client.get('/api/instituciones/99/rutas/1/estudiantes/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], "La institución con ID 99 no existe.")
    
    @patch('requests.get')
    def test_get_estudiantes_por_institucion_y_ruta_ruta_not_found(self, mock_get):
        # Mocking institution and route responses
        mock_get.side_effect = [
            MockResponse({"id": 1, "institucion_nombre": "Institucion 1"}, 200),
            MockResponse({"error": "La ruta con ID 99 no existe."}, 404)
        ]
        
        response = self.client.get('/api/instituciones/1/rutas/99/estudiantes/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json()['error'], "La ruta con ID 99 no existe.")

    @patch('requests.get')
    def test_get_estudiantes_por_institucion_y_ruta_route_not_associated(self, mock_get):
        # Mocking institution, route, and students data
        mock_get.side_effect = [
            MockResponse({"id": 1, "institucion_nombre": "Institucion 1"}, 200),
            MockResponse({"id": 1, "instituciones_ids": [2], "ruta_nombre": "Ruta 1"}, 200)
        ]
        
        response = self.client.get('/api/instituciones/1/rutas/1/estudiantes/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['error'], "La ruta con ID 1 no está asociada a la institución con ID 1.")

# Utility MockResponse class to mock requests responses
class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.exceptions.HTTPError(f'{self.status_code} Error')
