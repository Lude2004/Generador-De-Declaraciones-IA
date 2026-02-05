#-*- coding: utf-8 -*-

from typing import Optional, List, TYPE_CHECKING
from .component_metodologia import ComponentMetodologia

if TYPE_CHECKING:
    from domain.entidades import Persona, UsoIA

class Tarea(ComponentMetodologia):
    def __init__(self, descripcion: str):
        self.descripcion = descripcion
        self.responsable: Optional['Persona'] = None
        self.usos_ia: List['UsoIA'] = []

    def agregar_responsable(self, persona: 'Persona') -> None:
        self.responsable = persona

    def agregar_uso_ia(self, uso: 'UsoIA') -> None:
        self.usos_ia.append(uso)

    def remover_uso_ia(self, uso: UsoIA) -> None:
        if uso in self.usos_ia:
            self.usos_ia.remove(uso)

    def obtener_evidencias(self) -> List['UsoIA']:
        return self.usos_ia
    
    def mostrar_estructura(self, nivel = 0) -> None:
        sangria = "  " * nivel
        resp = f"[{self.responsable.nombre}]" if self.responsable else "[Sin Asignar]"
        print(f"{sangria}- Tarea: {self.descripcion} {resp}")
        for ia in self.usos_ia:
            print(f"{sangria}  * Uso IA: {ia}")
