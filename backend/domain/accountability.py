from django.db import models
from .tipo_responsabilidad import TipoResponsabilidad


class Accountability(models.Model):
    descripcion = models.TextField()
    tipo_responsabilidad = models.ForeignKey(TipoResponsabilidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion
