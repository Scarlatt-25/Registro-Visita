from django.shortcuts import render, redirect, get_object_or_404
from .models import Visita
from .forms import VisitaForm

# Inicio / Lista de visitas
def inicio(request):
    visitas = Visita.objects.all()
    return render(request, 'lista.html', {'visitas': visitas})

# Lista de visitas
def lista_visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'lista.html', {'visitas': visitas})

# Registrar visita
def registrar_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
    else:
        form = VisitaForm()
    return render(request, 'registrar.html', {'form': form})

# Editar visita
def editar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    if request.method == 'POST':
        form = VisitaForm(request.POST, instance=visita)
        if form.is_valid():
            form.save()
            return redirect('lista_visitas')
    else:
        form = VisitaForm(instance=visita)
    return render(request, 'editar.html', {'form': form})

# Eliminar visita
def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.delete()
    return redirect('lista_visitas')
