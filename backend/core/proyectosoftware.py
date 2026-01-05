#-*- coding: utf-8 -*-

from typing import Optional
from .equipo import Equipo
from .metodologia import Metodologia


class ProyectoSoftware:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.equipo = Equipo()
        self.metodologia: Optional[Metodologia] = None

    def seguir_metodologia(self, metodologia: Metodologia):
        self.metodologia = metodologia