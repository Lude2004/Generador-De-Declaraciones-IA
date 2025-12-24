from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Proyecto, Declaracion, HerramientaIA
from .serializers import ProyectoSerializer, DeclaracionSerializer

class ProyectoCreateView(APIView):
    def post(self, request):
        serializer = ProyectoSerializer(data=request.data)
        if serializer.is_valid():
            proyecto = serializer.save()
            return Response(
                ProyectoSerializer(proyecto).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GenerarDeclaracionView(APIView):
    def post(self, request):
        proyecto_id = request.data.get("proyecto_id")
        herramientas_ids = request.data.get("herramientas")

        proyecto = Proyecto.objects.get(id=proyecto_id)
        declaracion = Declaracion.objects.create(proyecto=proyecto)

        for h_id in herramientas_ids:
            declaracion.herramientas.add(HerramientaIA.objects.get(id=h_id))

        texto = declaracion.generarTextoDeclaracion()

        return Response({
            "id": declaracion.id,
            "texto": texto
        })
