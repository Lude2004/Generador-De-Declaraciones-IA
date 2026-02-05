#-*- coding: utf-8 -*-

from typing import List
from .persona import Persona


class Equipo:
    def __init__(self):
        self.miembros: List[Persona] = []


    def agregar_miembro(self, persona: Persona) -> None:
        self.miembros.append(persona)

    def remover_miembro(self, persona: Persona) -> None:
        self.miembros.remove(persona)
        
    def listar_miembros(self) -> List[Persona]:
        return self.miembros

