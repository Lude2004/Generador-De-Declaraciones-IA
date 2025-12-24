#-*- coding: utf-8 -*-

from django.db import models
from .FaseSDLC import FaseSDLC

class Fase(models.Model):
    nombre = models.CharField(
        max_length=50,
        choices=[(fase.value, fase.value) for fase in FaseSDLC]
    )

    def __str__(self):
        return self.nombre
