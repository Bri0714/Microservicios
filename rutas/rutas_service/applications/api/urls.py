from rest_framework.routers import DefaultRouter
from .views import RutaListCreate

app_name = 'ruta_app'

# Crear el router y registrar la vista
router = DefaultRouter()
router.register(r'rutas', RutaListCreate, basename='ruta')

# Definir las URL del router
urlpatterns = router.urls