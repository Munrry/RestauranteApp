from django.contrib import admin
from .models import Mesero

@admin.register(Mesero)
class MeseroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'telefono', 'usuario')
    search_fields = ('nombre', 'telefono')
    list_filter = ('usuario',)

