#-*- coding: utf-8 -*-

from typing import Optional, TYPE_CHECKING
from .equipo import Equipo

if TYPE_CHECKING:
    from domain.metodologia import Metodologia

class ProyectoSoftware:
    def __init__(self, nombre: str, metodologia: 'Metodologia', equipo: Equipo):
        self.nombre = nombre
        self.metodologia = metodologia
        self.equipo = equipo