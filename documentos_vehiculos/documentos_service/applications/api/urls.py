
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DocumentoVehiculoViewSet

app_name = 'documentos_app'

router = DefaultRouter()
router.register(r'documentos', DocumentoVehiculoViewSet, basename='documento')

# Definir las URL del router
urlpatterns = router.urls
