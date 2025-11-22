from django.db import models
from django.utils import timezone
from .validators import validar_rut

class Visita(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True, validators=[validar_rut])
    motivo = models.TextField()
    fecha_de_visita = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.nombre} - {self.fecha_de_visita}"
