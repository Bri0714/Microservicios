from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests

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

        # Verificar si hay rutas asociadas a la institución
        rutas_asociadas = [ruta for ruta in rutas_data if ruta.get('institucion_id') == institucion_id]
        institucion_data['rutas'] = rutas_asociadas

        # Validar si no existen rutas asociadas
        if not rutas_asociadas:
            institucion_data['mensaje'] = "No hay rutas asociadas a esta institución."

        return Response(institucion_data, status=status.HTTP_200_OK)

# Nueva clase para obtener la información de los estudiantes asociados a una ruta y institucion especifica 

class EstudiantesPorInstitucionYRutaView(APIView):
    def get(self, request, institucion_id, ruta_id):
        try:
            print(f"Intentando obtener estudiantes para institucion_id={institucion_id}, ruta_id={ruta_id}")
            # Validar existencia de la institución
            institucion_response = requests.get(f'http://instituciones:8001/api/instituciones/{institucion_id}/')
            if institucion_response.status_code != 200:
                return Response({'error': f'La institución con ID {institucion_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)
            institucion_data = institucion_response.json()

            # Validar existencia de la ruta
            ruta_response = requests.get(f'http://rutas:8002/api/rutas/{ruta_id}/')
            if ruta_response.status_code != 200:
                return Response({'error': f'La ruta con ID {ruta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)
            ruta_data = ruta_response.json()

            # Validar que la ruta esté asociada a la institución
            if ruta_data.get('institucion_id') != institucion_id:
                return Response({'error': f'La ruta con ID {ruta_id} no está asociada a la institución con ID {institucion_id}.'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener estudiantes por institucion_id y ruta_id
            estudiantes_response = requests.get(f'http://estudiantes:8004/api/estudiantes/?colegio_id={institucion_id}&ruta_id={ruta_id}')
            if estudiantes_response.status_code != 200:
                print(f"Error obteniendo estudiantes: {estudiantes_response.text}")
                return Response({'error': 'Error fetching estudiantes', 'details': estudiantes_response.text}, status=estudiantes_response.status_code)

            estudiantes = estudiantes_response.json()

            # Filtrar solo los estudiantes que pertenecen a la institución y ruta especificada
            estudiantes_filtrados = [est for est in estudiantes if est['colegio_id'] == institucion_id and est['ruta_id'] == ruta_id]

            # Modificar la respuesta para que sea más fácil de consumir
            response_data = {
                "institucion": {
                    "id": institucion_id,
                    "nombre": institucion_data.get("institucion_nombre")
                },
                "ruta": {
                    "id": ruta_id,
                    "nombre": ruta_data.get("ruta_nombre")
                },
                "estudiantes": []
            }

            # Añadir los datos de los estudiantes
            for estudiante in estudiantes_filtrados:
                estudiante_data = {
                    "id": estudiante["id"],
                    "nombre": estudiante["estudiante_nombre"],
                    "apellido": estudiante["estudiante_apellido"],
                    "edad": estudiante["estudiante_edad"],
                    "curso": estudiante["estudiante_curso"],
                    "direccion": estudiante["estudiante_direccion"],
                    "colegio_id": estudiante["colegio_id"],
                    "ruta_id": estudiante["ruta_id"],
                    "acudiente": estudiante["acudiente"]
                }
                response_data["estudiantes"].append(estudiante_data)

            return Response(response_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {str(e)}")
            return Response({'error': 'Service request failed', 'details': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
