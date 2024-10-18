from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

# Clase original para obtener instituciones con rutas
class InstitucionesWithRutasView(APIView):
    def get(self, request):
        try:
            # Solicitar la información de rutas
            rutas_response = requests.get('http://rutas:8002/api/rutas/')
            rutas_response.raise_for_status()  # Levanta una excepción si el código de estado no es 200

        except requests.exceptions.ConnectionError:
            return Response({'error': 'Error de conexión al servicio de rutas'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout:
            return Response({'error': 'Tiempo de espera agotado al obtener rutas'}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.exceptions.RequestException as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        rutas = rutas_response.json()

        for ruta in rutas:
            institucion_id = ruta.get('institucion_id')
            try:
                # Solicitar la información de la institución para cada ruta
                institucion_response = requests.get(f'http://instituciones:8001/api/instituciones/{institucion_id}/')
                institucion_response.raise_for_status()

                # Solo agregar el ID y el nombre de la institución
                institucion_data = institucion_response.json()
                ruta['institucion'] = {
                    'id': institucion_data.get('id'),
                    'institucion_nombre': institucion_data.get('institucion_nombre')
                }
                
            except requests.exceptions.RequestException:
                ruta['institucion'] = None

        return Response(rutas, status=status.HTTP_200_OK)

# Nueva clase para obtener la información de una institución y sus rutas asociadas
class InstitutionWithRoutesView(APIView):
    def get(self, request, institucion_id):
        try:
            # Solicitar la información de la institución
            institucion_response = requests.get(f'http://instituciones:8001/api/instituciones/{institucion_id}/')
            institucion_response.raise_for_status()

            institucion_data = institucion_response.json()

        except requests.exceptions.ConnectionError:
            return Response({"error": "Error de conexión al servicio de instituciones"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout:
            return Response({"error": "Tiempo de espera agotado al obtener la institución"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            # Solicitar las rutas asociadas a la institución
            rutas_response = requests.get(f'http://rutas:8002/api/rutas/?institucion_id={institucion_id}')
            rutas_response.raise_for_status()

            rutas_data = rutas_response.json()

        except requests.exceptions.ConnectionError:
            return Response({"error": "Error de conexión al servicio de rutas"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout:
            return Response({"error": "Tiempo de espera agotado al obtener las rutas"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Unir los datos de la institución y las rutas
        institucion_data['rutas'] = rutas_data

        return Response(institucion_data, status=status.HTTP_200_OK)
