from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication
import requests

# Nueva clase para obtener la información de una institución y sus rutas asociadas
#class InstitutionWithRoutesView(APIView):
#    authentication_classes = [JWTAuthentication]  # Utilizamos la autenticación JWT
#    permission_classes = [IsAuthenticated]  # Aseguramos que solo usuarios autenticados puedan acceder
#
#    def get(self, request, institucion_id):
#        try:
#            # Solicitar la información de la institución
#            institucion_response = requests.get(
#                f'http://instituciones:8001/api/instituciones/{institucion_id}/',
#                headers={"Authorization": request.headers.get("Authorization")}
#            )
#            if institucion_response.status_code == 404:
#                return Response({"error": "La institución con el ID proporcionado no existe."}, status=status.HTTP_404_NOT_FOUND)
#            institucion_response.raise_for_status()
#
#            institucion_data = institucion_response.json()
#
#        except requests.exceptions.ConnectionError:
#            return Response({"error": "Error de conexión al servicio de instituciones"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#        except requests.exceptions.Timeout:
#            return Response({"error": "Tiempo de espera agotado al obtener la institución"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
#
#        except requests.exceptions.RequestException as e:
#            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#        try:
#            # Solicitar las rutas asociadas a la institución
#            rutas_response = requests.get(
#                f'http://rutas:8002/api/rutas/?instituciones_ids={institucion_id}',
#                headers={"Authorization": request.headers.get("Authorization")}
#            )
#            rutas_response.raise_for_status()
#
#            rutas_data = rutas_response.json()
#
#        except requests.exceptions.ConnectionError:
#            return Response({"error": "Error de conexión al servicio de rutas"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
#
#        except requests.exceptions.Timeout:
#            return Response({"error": "Tiempo de espera agotado al obtener las rutas"}, status=status.HTTP_504_GATEWAY_TIMEOUT)
#
#        except requests.exceptions.RequestException as e:
#            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#        # Filtrar y mostrar solo las rutas que están asociadas a la institución actual
#        rutas_asociadas = []
#        for ruta in rutas_data:
#            if institucion_id in ruta.get('instituciones_ids', []):
#                ruta['instituciones'] = [
#                    institucion for institucion in ruta.get('instituciones', []) if institucion.get('id') == institucion_id
#                ]
#                rutas_asociadas.append(ruta)
#
#        institucion_data['rutas'] = rutas_asociadas
#
#        # Validar si no existen rutas asociadas
#        if not institucion_data['rutas']:
#            institucion_data['mensaje'] = "No hay rutas asociadas a esta institución."
#
#        return Response(institucion_data, status=status.HTTP_200_OK)


# Nueva clase para obtener la información de una institución y sus rutas asociadas, incluyendo vehículos y conductores
class InstitutionWithRoutesView(APIView):
    authentication_classes = [JWTAuthentication]  # Utilizamos la autenticación JWT
    permission_classes = [IsAuthenticated]  # Aseguramos que solo usuarios autenticados puedan acceder

    def get(self, request, institucion_id):
        try:
            # Solicitar la información de la institución
            institucion_response = requests.get(
                f'http://instituciones:8001/api/instituciones/{institucion_id}/',
                headers={"Authorization": request.headers.get("Authorization")}
            )
            if institucion_response.status_code == 404:
                return Response({"error": "La institución con el ID proporcionado no existe."}, status=status.HTTP_404_NOT_FOUND)
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
            rutas_response = requests.get(
                f'http://rutas:8002/api/rutas/?instituciones_ids={institucion_id}',
                headers={"Authorization": request.headers.get("Authorization")}
            )
            rutas_response.raise_for_status()

            rutas_data = rutas_response.json()

        except requests.exceptions.ConnectionError:
            return Response({"error": "Error de conexión al servicio de rutas"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        except requests.exceptions.Timeout:
            return Response({"error": "Tiempo de espera agotado al obtener las rutas"}, status=status.HTTP_504_GATEWAY_TIMEOUT)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Filtrar y mostrar solo las rutas que están asociadas a la institución actual
        rutas_asociadas = []
        for ruta in rutas_data:
            if institucion_id in ruta.get('instituciones_ids', []):
                ruta['instituciones'] = [
                    institucion for institucion in ruta.get('instituciones', []) if institucion.get('id') == institucion_id
                ]

                # Obtener información adicional de vehículos y conductores para cada ruta
                ruta_id = ruta.get("id")
                headers = {"Authorization": request.headers.get("Authorization")}

                # Obtener vehículo asociado a la ruta
                vehiculo_response = requests.get(
                    f'http://vehiculos:8006/api/vehiculos/',
                    headers=headers
                )
                if vehiculo_response.status_code == 200:
                    vehiculos = vehiculo_response.json()
                    for vehiculo_data in vehiculos:
                        if vehiculo_data.get("ruta_id") == ruta_id:
                            ruta["vehiculo"] = {
                                "placa": vehiculo_data.get("vehiculo_placa"),
                                "marca": vehiculo_data.get("vehiculo_marca"),
                                "modelo": vehiculo_data.get("vehiculo_modelo")
                            }

                            # Obtener conductor asociado al vehículo
                            vehiculo_id = vehiculo_data.get("id")
                            conductor_response = requests.get(
                                f'http://conductores:8005/api/conductores/',
                                headers=headers
                            )
                            if conductor_response.status_code == 200:
                                conductores = conductor_response.json()
                                for conductor_data in conductores:
                                    if conductor_data.get("vehiculo_id") == vehiculo_id:
                                        ruta["conductor"] = {
                                            "nombre": f"{conductor_data.get('nombre')} {conductor_data.get('apellido')}",
                                            "foto": conductor_data.get("foto"),
                                            "telefono": conductor_data.get("telefono")
                                        }
                            break  # Detener la búsqueda después de encontrar el vehículo asociado

                # Si no se encontró un vehículo asociado, añadir mensaje por defecto
                if "vehiculo" not in ruta:
                    ruta["vehiculo"] = "La ruta no tiene vehículo asociado"
                if "conductor" not in ruta:
                    ruta["conductor"] = "El vehículo no tiene conductor asociado"

                rutas_asociadas.append(ruta)

        institucion_data['rutas'] = rutas_asociadas

        # Validar si no existen rutas asociadas
        if not institucion_data['rutas']:
            institucion_data['mensaje'] = "No hay rutas asociadas a esta institución."

        return Response(institucion_data, status=status.HTTP_200_OK)

# Nueva clase para obtener la información de los estudiantes asociados a una ruta y institución específica
class EstudiantesPorInstitucionYRutaView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, institucion_id, ruta_id):
        try:
            # Validar existencia de la institución
            institucion_response = requests.get(
                f'http://instituciones:8001/api/instituciones/{institucion_id}/',
                headers={"Authorization": request.headers.get("Authorization")}
            )
            if institucion_response.status_code != 200:
                return Response({'error': f'La institución con ID {institucion_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)
            institucion_data = institucion_response.json()

            # Validar existencia de la ruta
            ruta_response = requests.get(
                f'http://rutas:8002/api/rutas/{ruta_id}/',
                headers={"Authorization": request.headers.get("Authorization")}
            )
            if ruta_response.status_code != 200:
                return Response({'error': f'La ruta con ID {ruta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)
            ruta_data = ruta_response.json()

            # Validar que la ruta esté asociada a la institución
            if institucion_id not in ruta_data.get('instituciones_ids', []):
                return Response({'error': f'La ruta con ID {ruta_id} no está asociada a la institución con ID {institucion_id}.'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener estudiantes por institucion_id y ruta_id
            estudiantes_response = requests.get(
                f'http://estudiantes:8004/api/estudiantes/?colegio_id={institucion_id}&ruta_id={ruta_id}',
                headers={"Authorization": request.headers.get("Authorization")}
            )
            if estudiantes_response.status_code != 200:
                return Response({'error': 'Error al obtener estudiantes', 'details': estudiantes_response.text}, status=estudiantes_response.status_code)

            estudiantes = estudiantes_response.json()

            # Filtrar solo los estudiantes que pertenecen a la institución y ruta especificada
            estudiantes_filtrados = [est for est in estudiantes if est['colegio_id'] == institucion_id and est['ruta_id'] == ruta_id]

            # Obtener el vehículo asociado a la ruta
            vehiculo_response = requests.get(
                f'http://vehiculos:8006/api/vehiculos/?ruta_id={ruta_id}',
                headers={"Authorization": request.headers.get("Authorization")}
            )
            if vehiculo_response.status_code != 200:
                return Response({'error': 'Error al obtener el vehículo asociado a la ruta', 'details': vehiculo_response.text}, status=vehiculo_response.status_code)

            vehiculos = vehiculo_response.json()
            # Filtrar el vehículo que corresponde a la ruta_id
            vehiculos_ruta = [v for v in vehiculos if v.get('ruta_id') == ruta_id]
            if not vehiculos_ruta:
                return Response({'error': f'No se encontró un vehículo asociado a la ruta con ID {ruta_id}.'}, status=status.HTTP_404_NOT_FOUND)

            vehiculo_data = vehiculos_ruta[0]

            # Modificar la respuesta para que sea más fácil de consumir
            response_data = {
                "institucion": {
                    "id": institucion_id,
                    "nombre": institucion_data.get("institucion_nombre"),
                    "nit": institucion_data.get("institucion_nit"),
                    "logo": institucion_data.get("institucion_logo")
                },
                "ruta": {
                    "id": ruta_id,
                    "nombre": ruta_data.get("ruta_nombre")
                },
                "vehiculo": vehiculo_data,
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
            return Response({'error': 'Error en la solicitud a un servicio externo', 'details': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': 'Ocurrió un error inesperado', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Nueva clase para obtener la información completa de una ruta, vehículo, conductor y monitora
class RutaVehiculoConductorView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, ruta_id):
        try:
            headers = {"Authorization": request.headers.get("Authorization")}

            # Validar existencia de la ruta
            ruta_response = requests.get(
                f'http://rutas:8002/api/rutas/{ruta_id}/',
                headers=headers
            )
            if ruta_response.status_code != 200:
                return Response({'error': f'La ruta con ID {ruta_id} no existe.'}, status=status.HTTP_404_NOT_FOUND)
            ruta_data = ruta_response.json()

            # Inicializar datos para la respuesta
            response_data = {
                "ruta": {
                    "id": ruta_id,
                    "nombre": ruta_data.get("ruta_nombre"),
                    "codigo": ruta_data.get("ruta_movil"),
                    "estado": ruta_data.get("activa")
                },
                "instituciones": "La ruta no tiene instituciones asociadas",
                "vehiculo": "La ruta no tiene vehículo asociado",
                "conductor": "El vehículo no tiene conductor asociado",
                "monitora": "El vehículo no tiene monitora asociada"
            }

            # Obtener instituciones asociadas a la ruta
            instituciones_ids = ruta_data.get('instituciones_ids', [])
            if instituciones_ids:
                instituciones = []
                for institucion_id in instituciones_ids:
                    institucion_response = requests.get(
                        f'http://instituciones:8001/api/instituciones/{institucion_id}/',
                        headers=headers
                    )
                    if institucion_response.status_code == 200:
                        institucion_data = institucion_response.json()
                        instituciones.append(institucion_data.get("institucion_nombre", "Nombre no disponible"))
                if instituciones:
                    response_data["instituciones"] = instituciones

            # Validar existencia del vehículo asociado a la ruta
            vehiculo_response = requests.get(
                f'http://vehiculos:8006/api/vehiculos/',
                headers=headers
            )
            if vehiculo_response.status_code == 200:
                vehiculos = vehiculo_response.json()
                for vehiculo_data in vehiculos:
                    if vehiculo_data.get("ruta_id") == ruta_id:  # Verificar que el vehículo esté asociado a la ruta actual
                        response_data["vehiculo"] = {
                            "placa": vehiculo_data.get("vehiculo_placa"),
                            "marca": vehiculo_data.get("vehiculo_marca"),
                            "modelo": vehiculo_data.get("vehiculo_modelo"),
                            "capacidad" : vehiculo_data.get("vehiculo_capacidad"),
                            "imagen": vehiculo_data.get("vehiculo_imagen")
                        }

                        # Validar existencia del conductor asociado al vehículo
                        vehiculo_id = vehiculo_data.get("id")
                        conductor_response = requests.get(
                            f'http://conductores:8005/api/conductores/',
                            headers=headers
                        )
                        if conductor_response.status_code == 200:
                            conductores = conductor_response.json()
                            for conductor_data in conductores:
                                if conductor_data.get("vehiculo_id") == vehiculo_id:  # Verificar que el conductor esté asociado al vehículo actual
                                    response_data["conductor"] = {
                                        "nombre": f"{conductor_data.get('nombre')} {conductor_data.get('apellido')}",
                                        "foto": conductor_data.get("foto"),
                                        "edad": conductor_data.get("edad"),
                                        "telefono": conductor_data.get("telefono"),
                                        "fecha_expedicion": conductor_data.get("fecha_exp"),
                                        "estado": conductor_data.get("licencia_activa")
                                    }

                        # Validar existencia de la monitora asociada al vehículo
                        monitora_data = vehiculo_data.get("monitora")
                        if monitora_data:
                            response_data["monitora"] = {
                                "nombre_completo": monitora_data.get("nombre_completo"),
                                "edad": monitora_data.get("edad"),
                                "telefono": monitora_data.get("telefono")
                            }

                        break  # Si encontramos el vehículo asociado, no es necesario seguir iterando

            return Response(response_data, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({'error': 'Service request failed', 'details': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except Exception as e:
            return Response({'error': 'An unexpected error occurred', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    