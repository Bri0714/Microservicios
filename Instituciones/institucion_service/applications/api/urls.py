from rest_framework.routers import DefaultRouter
from .views import InstitucionViewSet

app_name = 'institucion_app'

# Crear el router y registrar la vista
router = DefaultRouter()
router.register(r'instituciones', InstitucionViewSet, basename='institucion')

# Definir las URL del router
urlpatterns = router.urls
