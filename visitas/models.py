from django.db import models
from .validators import validar_rut

class Visita(models.Model):
    SERVICIOS_CHOICES = [
        ('corte', 'Corte de cabello'),
        ('tintura', 'Tintura'),
        ('manicure', 'Manicure'),
        ('pedicure', 'Pedicure'),
        ('alisado', 'Alisado'),
        ('peinado', 'Peinado'),
        ('perfilado de cejas', 'Perfilado de cejas'),
        ('lifting de pestañas', 'Lifting de pestañas'),
    ]

    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, validators=[validar_rut])
    servicio = models.CharField(max_length=50, choices=SERVICIOS_CHOICES)
    precio = models.IntegerField()
    fecha_visita = models.DateField()

    def __str__(self):
        return f"{self.cliente} - {self.servicio}"
