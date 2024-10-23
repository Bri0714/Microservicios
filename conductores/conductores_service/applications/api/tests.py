# tests.py para el servicio de conductores
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Conductor
from .serializers import ConductorSerializer
from datetime import date, timedelta

# Pruebas para el modelo Conductor
class ConductorModelTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del modelo Conductor
        self.conductor_data = {
            'nombre': 'Carlos',
            'apellido': 'Gomez',
            'edad': 35,
            'telefono': '1234567890',
            'fecha_exp': date.today() - timedelta(days=365),
            'licencia_activa': True
        }

    def test_create_conductor(self):
        # Verifica que se pueda crear un conductor y que se guarde correctamente
        conductor = Conductor.objects.create(**self.conductor_data)
        self.assertIsInstance(conductor, Conductor)
        self.assertEqual(conductor.nombre, 'Carlos')

    def test_conductor_str(self):
        # Verifica que el método __str__ del modelo Conductor devuelva el nombre y apellido del conductor
        conductor = Conductor.objects.create(**self.conductor_data)
        self.assertEqual(str(conductor), f"{conductor.nombre} {conductor.apellido}")

# Pruebas para la API de Conductores
class ConductorAPITestCase(APITestCase):
    def setUp(self):
        # Configuración inicial para las pruebas de la API
        self.conductor_data = {
            'nombre': 'Carlos',
            'apellido': 'Gomez',
            'edad': 35,
            'telefono': '1234567890',
            'fecha_exp': date.today() - timedelta(days=365),
            'licencia_activa': True
        }
        # Crear un conductor inicial para probar las funcionalidades de actualización y eliminación
        self.conductor = Conductor.objects.create(**self.conductor_data)

    def test_create_conductor(self):
        # Verifica que se pueda crear un conductor a través de la API
        new_conductor_data = {
            'nombre': 'Juan',
            'apellido': 'Perez',
            'edad': 40,
            'telefono': '0987654321',
            'fecha_exp': date.today() - timedelta(days=400),
            'licencia_activa': True
        }
        response = self.client.post('/api/conductores/', new_conductor_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Error en la creación del conductor:", response.data)  # Imprimir errores si falla la creación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Conductor.objects.count(), 2)  # ya existe uno creado en setUp

    def test_get_conductor_list(self):
        # Verifica que la API pueda listar los conductores existentes
        response = self.client.get('/api/conductores/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_conductor(self):
        # Verifica que se pueda actualizar un conductor a través de la API
        updated_data = {'nombre': 'Carlos Actualizado'}
        response = self.client.patch(f'/api/conductores/{self.conductor.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Carlos Actualizado')

    def test_delete_conductor(self):
        # Verifica que se pueda eliminar un conductor a través de la API
        response = self.client.delete(f'/api/conductores/{self.conductor.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Conductor.objects.count(), 0)

# Pruebas para el Serializador ConductorSerializer
class ConductorSerializerTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del serializador
        self.conductor_data = {
            'nombre': 'Carlos',
            'apellido': 'Gomez',
            'edad': 35,
            'telefono': '1234567890',
            'fecha_exp': date.today() - timedelta(days=365),
            'licencia_activa': True
        }

    def test_valid_data(self):
        # Verifica que el serializador sea válido con datos correctos
        serializer = ConductorSerializer(data=self.conductor_data)
        if not serializer.is_valid():
            print(serializer.errors)  # Imprimir errores si no es válido
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        # Verifica que el serializador no sea válido si los datos son incorrectos
        invalid_data = self.conductor_data.copy()
        invalid_data['telefono'] = 'not-a-phone-number'  # Formato de teléfono inválido
        serializer = ConductorSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('telefono', serializer.errors)
