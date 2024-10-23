from rest_framework.routers import DefaultRouter
from .views import InstitucionViewSet

app_name = 'conductor_app'

# Crear el router y registrar la vista
router = DefaultRouter()
router.register(r'conductores', InstitucionViewSet, basename='conductor')

# Definir las URL del router
urlpatterns = router.urls
