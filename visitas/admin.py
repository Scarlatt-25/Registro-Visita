from django.contrib import admin
from django.utils import timezone
from .models import Visita


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'rut', 'servicio', 'fecha_visita')
    search_fields = ('cliente', 'rut')
    list_filter = ('fecha_visita',)
    ordering = ('cliente',)
    list_per_page = 25
    actions = ['marcar_salida']

    @admin.action(description="Marcar nueva fecha de visita (actualizar fecha_visita = ahora) para las seleccionadas")
    def marcar_salida(self, request, queryset):
        pendientes = queryset.filter(fecha_visita__isnull=True)
        updated = pendientes.update(fecha_visita=timezone.now())
        self.message_user(request, f"{updated} visita actualizadas con nueva fecha de visita.")