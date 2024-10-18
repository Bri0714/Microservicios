from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from applications.api.models import Institucion
from applications.api.serializers import InstitucionSerializer

# Pruebas para el modelo Institucion
class InstitucionModelTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del modelo Institucion
        self.institution_data = {
            'institucion_nombre': 'Colegio San Jose',
            'institucion_nit': '901.316.552',
            'institucion_direccion': 'Calle 123 #45-67',
            'institucion_contactos': 'contacto@colegiosanjose.edu.co',
            'institucion_telefono': '1234567890'
        }

    def test_create_institution(self):
        # Verifica que se pueda crear una institución y que se guarde correctamente
        institution = Institucion.objects.create(**self.institution_data)
        self.assertIsInstance(institution, Institucion)
        self.assertEqual(institution.institucion_nombre, 'Colegio San Jose')

    def test_institution_str(self):
        # Verifica que el método __str__ del modelo Institucion devuelva el nombre de la institución
        institution = Institucion.objects.create(**self.institution_data)
        self.assertEqual(str(institution), f"{institution.institucion_nombre},{institution.institucion_nit}")

# Pruebas para la API de Instituciones
class InstitucionAPITestCase(APITestCase):
    def setUp(self):
        # Configuración inicial para las pruebas de la API
        self.institution_data = {
            'institucion_nombre': 'Colegio San Jose',
            'institucion_nit': '901.316.552',
            'institucion_direccion': 'Calle 123 #45-67',
            'institucion_contactos': 'contacto@colegiosanjose.edu.co',
            'institucion_telefono': '1234567890'
        }
        # Crear una institución inicial para probar las funcionalidades de actualización y eliminación
        self.institution = Institucion.objects.create(**self.institution_data)

    def test_create_institution(self):
        # Verifica que se pueda crear una institución a través de la API
        new_institution_data = {
            'institucion_nombre': 'Colegio Nuevo',
            'institucion_nit': '901.999.999',
            'institucion_direccion': 'Calle 456 #78-90',
            'institucion_contactos': 'contacto@colegionuevo.edu.co',
            'institucion_telefono': '0987654321'
        }
        response = self.client.post('/api/instituciones/', new_institution_data, format='json')
        if response.status_code != status.HTTP_201_CREATED:
            print("Error en la creación de la institución:", response.data)  # Imprimir errores si falla la creación
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Institucion.objects.count(), 2)  # ya existe uno creado en setUp

    def test_get_institution_list(self):
        # Verifica que la API pueda listar las instituciones existentes
        response = self.client.get('/api/instituciones/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_institution(self):
        # Verifica que se pueda actualizar una institución a través de la API
        updated_data = {'institucion_nombre': 'Colegio San Jose Actualizado'}
        response = self.client.patch(f'/api/instituciones/{self.institution.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['institucion_nombre'], 'Colegio San Jose Actualizado')

    def test_delete_institution(self):
        # Verifica que se pueda eliminar una institución a través de la API
        response = self.client.delete(f'/api/instituciones/{self.institution.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Institucion.objects.count(), 0)

# Pruebas para el Serializador InstitucionSerializer
class InstitucionSerializerTest(TestCase):
    def setUp(self):
        # Configuración inicial para las pruebas del serializador
        self.institution_data = {
            'institucion_nombre': 'Colegio San Jose',
            'institucion_nit': '901.316.552',
            'institucion_direccion': 'Calle 123 #45-67',
            'institucion_contactos': 'contacto@colegiosanjose.edu.co',
            'institucion_telefono': '1234567890'
        }

    def test_valid_data(self):
        # Verifica que el serializador sea válido con datos correctos
        serializer = InstitucionSerializer(data=self.institution_data)
        if not serializer.is_valid():
            print(serializer.errors)  # Imprimir errores si no es válido
        self.assertTrue(serializer.is_valid())

    def test_invalid_data(self):
        # Verifica que el serializador no sea válido si los datos son incorrectos
        invalid_data = self.institution_data.copy()
        invalid_data['institucion_contactos'] = 'not-an-email'  # Formato de correo electrónico inválido
        serializer = InstitucionSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('institucion_contactos', serializer.errors)