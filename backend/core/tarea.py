#-*- coding: utf-8 -*-

from typing import Optional
from .herramientaia import HerramientaIA


class Tarea:
    def __init__(self, nombre: str, descripcion: str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.seleccionada: bool = False
        self.herramienta_ia: Optional[HerramientaIA] = None

    def asignar_herramienta(self, herramienta: HerramientaIA):
        if self.seleccionada:
            self.herramienta_ia = herramienta
            return True
        else:
            raise ValueError(f"No se puede asignar la herramienta IA a '{self.nombre}' porque no está seleccionada.")

