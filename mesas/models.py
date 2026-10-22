from django.db import models

class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad = models.PositiveIntegerField(default=4)
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa #{self.numero}"
