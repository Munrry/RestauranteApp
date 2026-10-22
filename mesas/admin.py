from django.contrib import admin
from .models import Mesa

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('id', 'numero', 'capacidad', 'ocupada')
    search_fields = ('numero',)
    list_filter = ('ocupada', 'capacidad')