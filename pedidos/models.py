from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Plato(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='platos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=4)
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa #{self.numero}"

class Mesero(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.nombre

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
    platos = models.ManyToManyField(Plato, through='DetallePedido')

    def __str__(self):
        return f"Pedido #{self.id} - Mesa {self.mesa.numero} ({self.get_estado_display()})"

    @property
    def total_pedido(self):
        return sum(detalle.subtotal for detalle in self.detalles.all())

class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    observacion = models.CharField(max_length=255, blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        if not self.precio_unitario:
            self.precio_unitario = self.plato.precio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad}x {self.plato.nombre} (Pedido #{self.pedido.id})"