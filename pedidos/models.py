from django.db import models
from mesas.models import Mesa
from meseros.models import Mesero
from platos.models import Plato

class Pedido(models.Model):
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('EN_PREPARACION', 'En Preparación'),
        ('LISTO', 'Listo para Servir'),
        ('PAGADO', 'Pagado / Cerrado'),
        ('CANCELADO', 'Cancelado'),
    ]

    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='pedidos')
    mesero = models.ForeignKey(Mesero, on_delete=models.CASCADE, related_name='pedidos')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    platos = models.ManyToManyField(Plato, through='detalles_pedido.DetallePedido')

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero} ({self.get_estado_display()})"

    @property
    def total_pedido(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())