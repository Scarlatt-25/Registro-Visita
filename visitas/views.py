from django.shortcuts import render, redirect, get_object_or_404
from .models import Visita
from .forms import VisitaForm
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer, VisitaSerializer
from .ai import analizar_visita_con_ia
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


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
            return redirect('visitas_lista')
    else:
        form = VisitaForm()

    visitas = Visita.objects.all()

    return render(request, 'registrar.html', {
        'form': form,
        'visitas': visitas
    })


def lista_visitas(request):
    visitas = Visita.objects.all()
    return render(request, 'lista.html', {'visitas': visitas})


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


def eliminar_visita(request, id):
    visita = get_object_or_404(Visita, id=id)
    visita.delete()
    return redirect('lista_visitas')


@csrf_exempt
def sugerir_servicio(request):
    if request.method == "POST":
        pregunta = request.POST.get("pregunta")

        if not pregunta:
            return JsonResponse({"respuesta": "Escribe algo po 😅"})

        respuesta = analizar_visita_con_ia(
            cliente="Cliente",
            servicio=pregunta
        )

        return JsonResponse({"respuesta": respuesta})

    return JsonResponse({"respuesta": "Método no permitido"}, status=405)