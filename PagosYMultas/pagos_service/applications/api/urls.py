# pagos_multas/urls.py

from rest_framework.routers import DefaultRouter
from .views import PagoViewSet

app_name = 'pago_app'

router = DefaultRouter()
router.register(r'pagos', PagoViewSet, basename='pago')

urlpatterns = router.urls