from django.contrib import admin
from .models import Categoria, Plato, Mesa, Mesero, Pedido, DetallePedido

class DetallePedidoInline(admin.TabularInline):
    model = DetallePedido
    extra = 1

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'mesa', 'mesero', 'estado', 'fecha_creacion', 'total_pedido')
    list_filter = ('estado', 'fecha_creacion', 'mesero')
    inlines = [DetallePedidoInline]

admin.site.register(Categoria)
admin.site.register(Plato)
admin.site.register(Mesa)
admin.site.register(Mesero)