from django.contrib import admin
from .models import Pedido
from detalles_pedido.models import DetallePedido

# Personalización del título del panel de administración
admin.site.site_header = "Administración de RestauranteApp"
admin.site.site_title = "Portal de Administración"
admin.site.index_title = "Panel de Control y Gestión"

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 0

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'mesero', 'estado', 'fecha_creacion', 'total_pedido')
    list_filter = ('estado', 'mesero', 'mesa')
    search_fields = ('id', 'mesa__numero', 'mesero__nombre')
    inlines = [DetallePedidoInline]