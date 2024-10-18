from django.contrib import admin
from .models import Ruta

@admin.register(Ruta)

# Register your models here.
class RutaAdmin(admin.ModelAdmin):
    list_display = (
        'ruta_movil',
        'institucion_id',
        'activa'
    )