#-*- coding: utf-8 -*-

from datetime import date
from typing import List

class DeclaracionIA:
    def __init__(self):
        self.fecha_emision = date.today()
        self.contenido: List[str] = []
    
    def generar(self) -> None:
        print(f"\n--- REPORTE DECLARACIÓN IA ({self.fecha_emision}) ---")
        for linea in self.contenido:
            print(linea)
        print("----------------------------------------------------")