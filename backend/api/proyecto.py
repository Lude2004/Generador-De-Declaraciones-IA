#-*- coding: utf-8 -*-

from django.db import models

class Proyecto(models.Model):
    titulo = models.CharField(max_length=200)
    lider = models.CharField(max_length=100)
    metodologia = models.CharField(max_length=100)

    def __str__(self):
        return self.titulo
