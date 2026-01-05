#-*- coding: utf-8 -*-

from typing import List
from .MetodologiaAgil import MetodologiaAgil
from .fase import Fase


class Metodologia:
    def __init__(self, nombre: MetodologiaAgil):
        self.nombre = nombre.value
        self.fases: List[Fase] = []

    def obtener_fases(self) -> List[Fase]:
        return self.fases
    
    def agregar_fase(self, fase: Fase):
        self.fases.append(fase)
