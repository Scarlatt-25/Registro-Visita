from django.shortcuts import render, redirect, get_object_or_404
from .models import Visita
from .forms import VisitaForm
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer, VisitaSerializer


class VisitaViewSet(viewsets.ModelViewSet):
    queryset = Visita.objects.all()
    serializer_class = VisitaSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


def inicio(request):
    visitas = Visita.objects.all()
    return render(request, 'lista.html', {'visitas': visitas})


def registrar_visita(request):
    if request.method == 'POST':
        form = VisitaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visitas_lista')  # lista bien hecha
    else:
        form = VisitaForm()

    visitas = Visita.objects.all()  # para mostrar la tabla en registrar.html

    return render(request, 'registrar.html', {
        'form': form,
        'visitas': visitas
    })


def lista_visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'lista.html', {'visitas': visitas})

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