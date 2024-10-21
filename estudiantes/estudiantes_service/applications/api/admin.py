from django.contrib import admin
from .models import Estudiante,Acudiente
# Register your models here.

#admin.site.register(Institucion)

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = (
        'estudiante_nombre',
        'estudiante_apellido',
        'estudiante_edad',
        'estudiante_curso',
)
    
@admin.register(Acudiente)
class AcudienteAdmin(admin.ModelAdmin):
    list_display = (
        'acudiente_nombre',
        'acudiente_apellido',
        'acudiente_parentesco',
        'acudiente_telefono',
    )