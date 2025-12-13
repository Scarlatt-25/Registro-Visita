from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='lista_visitas'),
    path('lista/', views.lista_visitas, name='visitas_lista'),
    path('registrar/', views.registrar_visita, name='visitas_registrar'),
    path('editar/<int:id>/', views.editar_visita, name='visitas_editar'),
    path('eliminar/<int:id>/', views.eliminar_visita, name='visitas_eliminar'),
]

