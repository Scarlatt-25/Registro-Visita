from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ["nombre", "rut", "motivo", "fecha_de_visita"]
