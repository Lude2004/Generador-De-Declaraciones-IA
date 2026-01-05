#-*- coding: utf-8 -*-

from typing import List
from .tarea import Tarea


class Fase:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.tareas: List[Tarea] = []

    def obtener_tareas(self) -> List[Tarea]:
        return self.tareas


    def agregar_tarea(self, tarea: Tarea):
        self.tareas.append(tarea)
