# -*- coding: utf-8 -*-
from django.test import SimpleTestCase
from domain.tareas.component_metodologia import TareaHoja, FaseCompuesta
from domain.tareas.tarea import Tarea

class ConcreteTarea(Tarea):
    def obtener_nombre(self) -> str:
        return self.descripcion
    def obtener_descripcion(self) -> str:
        return self.descripcion
    def obtener_datos(self) -> dict:
        return {"descripcion": self.descripcion}

class CompositePatternTests(SimpleTestCase):
    def test_tarea_hoja_datos(self):
        tarea = TareaHoja("Tarea 1", "Descripción 1", "Seguridad")
        self.assertEqual(tarea.obtener_nombre(), "Tarea 1")
        self.assertEqual(tarea.obtener_descripcion(), "Descripción 1")
        self.assertEqual(tarea.categoria, "Seguridad")

        datos = tarea.obtener_datos()
        self.assertEqual(datos["nombre"], "Tarea 1")
        self.assertEqual(datos["tipo"], "tarea")

    def test_fase_compuesta(self):
        fase = FaseCompuesta("Fase Inicial", "Descripción de fase")
        tarea1 = TareaHoja("T1", "D1")
        tarea2 = TareaHoja("T2", "D2")

        fase.agregar_componente(tarea1)
        fase.agregar_componente(tarea2)

        self.assertEqual(fase.contar_tareas(), 2)
        self.assertEqual(len(fase.obtener_todas_tareas()), 2)

        fase.remover_componente(tarea1)
        self.assertEqual(fase.contar_tareas(), 1)

class DomainTareaTests(SimpleTestCase):
    def test_tarea_domain(self):
        tarea = ConcreteTarea("Implementar login")
        self.assertEqual(tarea.descripcion, "Implementar login")
        self.assertIsNone(tarea.responsable)
        self.assertEqual(len(tarea.usos_ia), 0)
