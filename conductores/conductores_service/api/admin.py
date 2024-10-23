# Register your models here.
from django.contrib import admin
from .models import Conductor
# Register your models here.

#admin.site.register(Institucion)

@admin.register(Conductor)
class InstitucionAdmin(admin.ModelAdmin):
    list_display = (
        'institucion_nombre',
        'institucion_direccion',
        'institucion_nit',
        'institucion_contactos',
        'institucion_telefono',
)
    