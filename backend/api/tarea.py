#-*- coding: utf-8 -*-

from django.db import models
from .fase import Fase

class Tarea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fase = models.ForeignKey(
        Fase,
        related_name="tareas",
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.nombre
