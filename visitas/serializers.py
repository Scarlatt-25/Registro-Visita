from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import Visita 
from .validators import validar_rut


class VisitaSerializers(serializers.HyperlinkedModelSerializer):

    def validate_rut(self, value):
        validar_rut(value)  # si hay error, lo lanza el validator
        return value

    class Meta:
        model = Visita
        fields = ["url", "nombre", "rut", "motivo", "fecha_de_visita"]


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model= User
        fields= ["url","username","email","groups"]

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group 
        fields =["url","name"]

