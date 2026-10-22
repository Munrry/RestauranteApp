from django.db import models

class DetallePedido(models.Model):
    pedido = models.ForeignKey('pedidos.Pedido', on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey('platos.Plato', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.cantidad * self.plato.precio

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre}"