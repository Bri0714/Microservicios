from rest_framework.routers import DefaultRouter
from .views import ConductorViewSet

app_name = 'conductor_app'

# Crear el router y registrar la vista
router = DefaultRouter()
router.register(r'conductores', ConductorViewSet, basename='conductor')

# Definir las URL del router
urlpatterns = router.urls
