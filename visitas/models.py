from django.db import models
from django.utils import timezone
from .validators import validar_rut

class Visita(models.Model):

    SERVICIOS_CHOICES = [
        ('corte', 'Corte de cabello'),
        ('tintura', 'Tintura'),
        ('manicure', 'Manicure'),
        ('pedicure', 'Pedicure'),
        ('alisado', 'Alisado'),
        ('peinado', 'Peinado'),
        ('prefilado de cejas','Perfilado de Cejas'),
        ('lifting de pestañas','Lifting de Pestañas'),
    ]

    PRECIOS_SERVICIOS = {
        'corte': 15000,
        'tintura': 25000,
        'manicure': 12000,
        'pedicure': 15000,
        'alisado': 30000,
        'peinado': 20000,
        'prefilado de cejas': 10000,
        'lifting de pestañas':18000,
    }


    cliente = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, validators=[validar_rut])
    servicio = models.CharField(max_length=50, choices=SERVICIOS_CHOICES)
    precio = models.IntegerField() 
    fecha_visita = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.cliente} - {self.servicio} (${self.precio})"
