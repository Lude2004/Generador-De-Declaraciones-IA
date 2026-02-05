#-*- coding: utf-8 -*-

from typing import List
from .component_metodologia import ComponentMetodologia

class Fase(ComponentMetodologia):
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.hijos: List[ComponentMetodologia] = []

    def agregar(self, componente: ComponentMetodologia) -> None:
        self.hijos.append(componente)

    def remover(self, componente: ComponentMetodologia) -> None:
        self.hijos.remove(componente)

    def obtener_hijos(self) -> List[ComponentMetodologia]:
        return self.hijos

    def mostrar_estructura(self, nivel: int = 0) -> None:
        sangria = "  " * nivel
        print(f"{sangria}+ FASE: {self.nombre}")
        for hijo in self.hijos:
            hijo.mostrar_estructura(nivel + 1)