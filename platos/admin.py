from django.contrib import admin
from .models import Plato

@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'categoria', 'precio', 'disponible')
    search_fields = ('nombre', 'categoria__nombre')
    list_filter = ('disponible', 'categoria')
# Register your models here.
