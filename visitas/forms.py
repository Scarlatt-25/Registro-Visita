from django import forms
from .models import Visita

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['cliente', 'rut', 'servicio', 'precio', 'fecha_visita']
        widgets = {
            'precio': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'fecha_visita': forms.DateInput(attrs={'type': 'date'}),
        }
