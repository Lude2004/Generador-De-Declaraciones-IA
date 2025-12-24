#-*- coding: utf-8 -*-

from django.db import models
from .proyecto import Proyecto

class MiembroEquipo(models.Model):
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)
    proyecto = models.ForeignKey(
        Proyecto,
        related_name="miembros",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.nombre - {self.nombre}}"
