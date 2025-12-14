from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['cliente', 'rut', 'servicio', 'precio', 'fecha_visita']
