from rest_framework.routers import DefaultRouter
from .views import VehiculoListCreate, MonitoraListCreate

app_name = 'vehiculo_app'

# Crear el router y registrar la vista
router = DefaultRouter()
router.register(r'vehiculos', VehiculoListCreate, basename='vehiculo')
router.register(r'monitoras', MonitoraListCreate, basename='monitora')


# Definir las URL del router
urlpatterns = router.urls