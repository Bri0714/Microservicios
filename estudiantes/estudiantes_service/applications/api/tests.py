from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from applications.api.models import Estudiante, Acudiente
from applications.api.serializers import EstudianteSerializer

# Pruebas para el modelo Estudiante
class EstudianteModelTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del modelo Estudiante
        self.acudiente_data = {
            'acudiente_nombre': 'Alexander',
            'acudiente_apellido': 'Díaz',
            'acudiente_parentesco': 'Padre',
            'acudiente_telefono': '123456789'
        }
        self.acudiente = Acudiente.objects.create(**self.acudiente_data)
        self.estudiante_data = {
            'acudiente': self.acudiente,
            'colegio_id': 1,
            'ruta_id': 1,
            'estudiante_nombre': 'Brian',
            'estudiante_apellido': 'Amezquita',
            'estudiante_edad': 17,
            'estudiante_curso': '9A',
            'estudiante_direccion': 'Calle 123'
        }

    def test_create_estudiante(self):
        # Verifica que se pueda crear un estudiante y que se guarde correctamente
        estudiante = Estudiante.objects.create(**self.estudiante_data)
        self.assertIsInstance(estudiante, Estudiante)
        self.assertEqual(estudiante.estudiante_nombre, 'Brian')

    def test_estudiante_str(self):
        # Verifica que el método __str__ del modelo Estudiante devuelva el nombre completo del estudiante
        estudiante = Estudiante.objects.create(**self.estudiante_data)
        self.assertEqual(str(estudiante), f"{estudiante.estudiante_nombre} {estudiante.estudiante_apellido}")

# Pruebas para la API de Estudiantes
class EstudianteAPITestCase(APITestCase):
    def setUp(self):
        # Configuración inicial para las pruebas de la API
        self.acudiente_data = {
            'acudiente_nombre': 'Alexander',
            'acudiente_apellido': 'Díaz',
            'acudiente_parentesco': 'Padre',
            'acudiente_telefono': '123456789'
        }
        self.acudiente = Acudiente.objects.create(**self.acudiente_data)
        self.estudiante_data = {
            'acudiente': self.acudiente,
            'colegio_id': 1,
            'ruta_id': 1,
            'estudiante_nombre': 'Brian',
            'estudiante_apellido': 'Amezquita',
            'estudiante_edad': 17,
            'estudiante_curso': '9A',
            'estudiante_direccion': 'Calle 123'
        }
        # Crear un estudiante inicial para probar las funcionalidades de actualización y eliminación
        self.estudiante = Estudiante.objects.create(**self.estudiante_data)

    def test_create_estudiante(self):
        # Verifica que se pueda crear un estudiante a través de la API
        new_estudiante_data = {
            'acudiente': {
                'acudiente_nombre': 'Katherine',
                'acudiente_apellido': 'Soler',
                'acudiente_parentesco': 'Madre',
                'acudiente_telefono': '987654321'
            },
            'colegio_id': 2,
            'ruta_id': 2,
            'estudiante_nombre': 'Sebastian',
            'estudiante_apellido': 'Soler',
            'estudiante_edad': 16,
            'estudiante_curso': '10B',
            'estudiante_direccion': 'Calle 456'
        }
        response = self.client.post('/api/estudiantes/', new_estudiante_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Error en la creación del estudiante:", response.data)  # Imprimir errores si falla la creación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Estudiante.objects.count(), 2)  # ya existe uno creado en setUp

    def test_get_estudiante_list(self):
        # Verifica que la API pueda listar los estudiantes existentes
        response = self.client.get('/api/estudiantes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_estudiante(self):
        # Verifica que se pueda actualizar un estudiante a través de la API
        updated_data = {'estudiante_nombre': 'Brian Alexander'}
        response = self.client.patch(f'/api/estudiantes/{self.estudiante.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estudiante_nombre'], 'Brian Alexander')

    def test_delete_estudiante(self):
        # Verifica que se pueda eliminar un estudiante a través de la API
        response = self.client.delete(f'/api/estudiantes/{self.estudiante.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Estudiante.objects.count(), 0)

# Pruebas para el Serializador EstudianteSerializer
class EstudianteSerializerTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del serializador
        self.acudiente_data = {
            'acudiente_nombre': 'Alexander',
            'acudiente_apellido': 'Díaz',
            'acudiente_parentesco': 'Padre',
            'acudiente_telefono': '123456789'
        }
        self.acudiente = Acudiente.objects.create(**self.acudiente_data)
        self.estudiante_data = {
            'acudiente': {
                'acudiente_nombre': 'Alexander',
                'acudiente_apellido': 'Díaz',
                'acudiente_parentesco': 'Padre',
                'acudiente_telefono': '123456789'
            },
            'colegio_id': 1,
            'ruta_id': 1,
            'estudiante_nombre': 'Brian',
            'estudiante_apellido': 'Amezquita',
            'estudiante_edad': 17,
            'estudiante_curso': '9A',
            'estudiante_direccion': 'Calle 123'
        }

    def test_valid_data(self):
        # Verifica que el serializador sea válido con datos correctos
        serializer = EstudianteSerializer(data=self.estudiante_data)
        if not serializer.is_valid():
            print(serializer.errors)  # Imprimir errores si no es válido
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        # Verifica que el serializador no sea válido si los datos son incorrectos
        invalid_data = self.estudiante_data.copy()
        invalid_data['estudiante_edad'] = -1  # Edad inválida
        serializer = EstudianteSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('estudiante_edad', serializer.errors)
