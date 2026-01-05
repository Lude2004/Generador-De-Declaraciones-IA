#-*- coding: utf-8 -*-

from typing import List
from .persona import Persona


class Equipo:
    def __init__(self):
        self.miembros: List[Persona] = []


    def agregar_miembro(self, persona: Persona):
        self.miembros.append(persona)
        
    def listar_miembros(self) -> List[Persona]:
        return self.miembros

