"""gateway_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import InstitutionWithRoutesView, EstudiantesPorInstitucionYRutaView, RutaVehiculoConductorView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Ruta para obtener una institución específica con sus rutas asociadas
    path('api/instituciones/<int:institucion_id>/rutas/', InstitutionWithRoutesView.as_view()),
    
    # Ruta para obtener los estudiantes de una institución y una ruta específica
    path('api/instituciones/<int:institucion_id>/rutas/<int:ruta_id>/estudiantes/', EstudiantesPorInstitucionYRutaView.as_view()),
    
    # Ruta para obtener la información completa de la ruta, vehículo y conductor
    path('api/rutas/<int:ruta_id>/', RutaVehiculoConductorView.as_view()),
    
]
