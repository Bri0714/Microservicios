from rest_framework.routers import DefaultRouter
from .views import EstudianteViewSet,AcudienteViewSet

app_name = 'estudiante_app'

# Crear el router y registrar la vista
router = DefaultRouter()
router.register(r'estudiantes', EstudianteViewSet, basename='estudiante')
router.register(r'acudientes', AcudienteViewSet, basename='acudiente')

# Definir las URL del router
urlpatterns = router.urls