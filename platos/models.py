from django.db import models
from categorias.models import Categoria

class Plato(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='platos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"