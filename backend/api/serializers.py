from rest_framework import serializers
from .models import Proyecto, MiembroEquipo
from .models import HerramientaIA
from .models import Declaracion

class MiembroEquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiembroEquipo
        fields = ['id', 'nombre', 'rol']

class ProyectoSerializer(serializers.ModelSerializer):
    miembros = MiembroEquipoSerializer(many=True)

    class Meta:
        model = Proyecto
        fields = ['id', 'titulo', 'lider', 'metodologia', 'miembros']

class HerramientaIASerializer(serializers.ModelSerializer):
    class Meta:
        model = HerramientaIA
        fields = ['id', 'nombre', 'version']

class DeclaracionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Declaracion
        fields = ['id', 'proyecto', 'herramientas', 'fecha_creacion', 'texto_generado']