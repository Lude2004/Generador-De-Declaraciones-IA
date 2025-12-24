from django.test import TestCase
from .models import Proyecto

class ProyectoTest(TestCase):
    def test_creacion_proyecto(self):
        p = Proyecto.objects.create(
            titulo = "Proyecto IA",
            lider = "Alexis Ludeña",
            metodologia = "MDA"
        )
        self.assertEqual(p.titulo, "Proyecto IA")
