from django.urls import path, include
from . import views
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"visitas", views.VisitaViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('inicio/', views.inicio, name='lista_visitas'),
    path('lista/', views.lista_visitas, name='visitas_lista'),
    path('registrar/', views.registrar_visita, name='visitas_registrar'),
    path('editar/<int:id>/', views.editar_visita, name='visitas_editar'),
    path('eliminar/<int:id>/', views.eliminar_visita, name='visitas_eliminar'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/sugerir-servicio/', views.sugerir_servicio, name='sugerir_servicio'),
]
