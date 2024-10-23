# Register your models here.
from django.contrib import admin
from .models import Conductor
# Register your models here.

#admin.site.register(Institucion)

@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'apellido',
        'edad',
        'telefono',
        'licencia_activa',
)
    
