#-*- coding: utf-8 -*-

from django.db import models
from datetime import datetime
from .proyecto import Proyecto
from .herramientaia import HerramientaIA

class Declaracion(models.Model):
    fechaCreacion = models.DateField(auto_now_add=True)
    texto_generado = models.TextField(blank=True)
    proyecto = models.ForeignKey(
        Proyecto,
        on_delete=models.CASCADE
    )
    herramientas = models.ManyToManyField(HerramientaIA)

    def generarTextoDeclaracion(self):
        meses = [
            "enero", "febrero", "marzo", "abril", "mayo", "junio",
            "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"
        ]
        hoy = datetime.now()
        fecha = f"{hoy.day} de {meses[hoy.month-1]} de {hoy.year}"

        equipo = ""
        for m in self.proyecto.miembros.all():
            equipo += f"{m.nombre} - {m.rol}\n"
        
        herramientas_txt = ""
        for h in self.herramientas.all():
            herramientas_txt += f"{h.nombre} {h.version}\n"

        self.texto_generado = f"""
        DECLARACIÓN DE USO DE IA GENERATIVA

        Fecha: {fecha}

        Proyecto: {self.proyecto.titulo}
        Líder: {self.proyecto.lider}
        Medotología: {self.proyecto.metodologia}

        Equipo:
        {equipo}

        Herramientas de IA utilizadas:
        {herramientas_txt}

        El equipo declara que las herramientas de IA fueron utilizadas como apoyo 
        en tareas específicas, manteniendo simpre control humano sobre el 
        resultado final.

        """

        self.save()

        return self.texto_generado

    def exportarDeclaracion(self, ):
        pass

