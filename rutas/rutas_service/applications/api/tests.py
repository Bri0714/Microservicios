from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from applications.api.models import Ruta
from applications.api.serializers import RutaSerializer

"""
- RutaModelTest: Verifica que el modelo de ruta funcione correctamente, que se pueda crear una ruta, y que el método __str__ funcione como se espera.
- RutaAPITestCase: Verifica que las operaciones CRUD funcionen correctamente en la API de rutas. Incluye pruebas para crear, listar, actualizar y eliminar rutas.
- RutaSerializerTest: Verifica que el serializador funcione correctamente. Se prueban casos de datos válidos e inválidos.
"""

# Pruebas para el modelo Ruta
class RutaModelTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del modelo Ruta
        self.ruta_data = {
            'ruta_nombre': 'Ruta 1',
            'ruta_movil': 12345,
            'institucion_id': 1,  # Este ID será simulado en los tests
            'activa': True
        }

    def test_create_ruta(self):
        # Verifica que se pueda crear una ruta y que se guarde correctamente
        ruta = Ruta.objects.create(**self.ruta_data)
        self.assertIsInstance(ruta, Ruta)
        self.assertEqual(ruta.ruta_nombre, 'Ruta 1')

    def test_ruta_str(self):
        # Verifica que el método __str__ del modelo Ruta devuelva el nombre y móvil de la ruta
        ruta = Ruta.objects.create(**self.ruta_data)
        self.assertEqual(str(ruta), f"{ruta.ruta_nombre} - {ruta.ruta_movil}")

# Pruebas para la API de Rutas
class RutaAPITestCase(APITestCase):

    @patch('applications.api.serializers.requests.get')  # Simula la solicitud al servicio de Instituciones
    def setUp(self, mock_get):
        # Simula que la institución existe en el servicio de Instituciones
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'institucion_nombre': 'Colegio San Jose',
            'institucion_nit': '901.316.552'
        }

        # Configuración inicial para las pruebas de la API
        self.ruta_data = {
            'ruta_nombre': 'Ruta 1',
            'ruta_movil': 12345,
            'institucion_id': 1,  # Usa el ID simulado
            'activa': True
        }
        # Crear una ruta inicial para probar las funcionalidades de actualización y eliminación
        self.ruta = Ruta.objects.create(**self.ruta_data)

    @patch('applications.api.serializers.requests.get')  # Simula la solicitud al servicio de Instituciones
    def test_create_ruta(self, mock_get):
        # Simula que la institución existe en el servicio de Instituciones
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'institucion_nombre': 'Colegio San Jose',
            'institucion_nit': '901.316.552'
        }

        # Verifica que se pueda crear una ruta a través de la API
        new_ruta_data = {
            'ruta_nombre': 'Ruta 2',
            'ruta_movil': 67890,
            'institucion_id': 1,  # Usa una institución simulada
            'activa': True
        }
        response = self.client.post('/api/rutas/', new_ruta_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Error en la creación de la ruta:", response.data)  # Imprimir errores si falla la creación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ruta.objects.count(), 2)  # ya existe una creada en setUp

    @patch('applications.api.serializers.requests.get')  # Simula que la institución no existe
    def test_create_ruta_institucion_not_found(self, mock_get):
        # Simula que la institución no existe en el servicio de Instituciones
        mock_get.return_value.status_code = 404

        # Intenta crear una ruta con una institución que no existe
        new_ruta_data = {
            'ruta_nombre': 'Ruta 3',
            'ruta_movil': 56789,
            'institucion_id': 999,  # ID que no existe
            'activa': True
        }
        response = self.client.post('/api/rutas/', new_ruta_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('institucion_id', response.data)
        self.assertEqual(Ruta.objects.count(), 1)  # No se debe crear la nueva ruta

    def test_get_ruta_list(self):
        # Verifica que la API pueda listar las rutas existentes
        response = self.client.get('/api/rutas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    @patch('applications.api.serializers.requests.get')
    def test_update_ruta(self, mock_get):
        # Simula la solicitud de la institución existente
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'institucion_nombre': 'Colegio San Jose',
            'institucion_nit': '901.316.552'
        }

        # Verifica que se pueda actualizar una ruta a través de la API
        updated_data = {'ruta_nombre': 'Ruta Actualizada'}
        response = self.client.patch(f'/api/rutas/{self.ruta.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['ruta_nombre'], 'Ruta Actualizada')

    def test_delete_ruta(self):
        # Verifica que se pueda eliminar una ruta a través de la API
        response = self.client.delete(f'/api/rutas/{self.ruta.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ruta.objects.count(), 0)

# Pruebas para el Serializador RutaSerializer
class RutaSerializerTest(TestCase):

    @patch('applications.api.serializers.requests.get')  # Simular la solicitud al servicio de Instituciones
    def setUp(self, mock_get):
        # Simula que la institución existe
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'id': 1,
            'institucion_nombre': 'Colegio Ejemplo',
            'institucion_nit': '901.999.999'
        }

        # Configuración inicial para las pruebas del serializador
        self.ruta_data = {
            'ruta_nombre': 'Ruta 1',
            'ruta_movil': 12345,
            'institucion_id': 1,
            'activa': True
        }

    def test_valid_data(self):
        # Verifica que el serializador sea válido con datos correctos
        serializer = RutaSerializer(data=self.ruta_data)
        if not serializer.is_valid():
            print(serializer.errors)  # Imprimir errores si no es válido
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        # Verifica que el serializador no sea válido si los datos son incorrectos
        invalid_data = self.ruta_data.copy()
        invalid_data['ruta_movil'] = 'not-a-number'  # Valor inválido para el número de móvil
        serializer = RutaSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('ruta_movil', serializer.errors)
