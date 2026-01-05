#-*- coding: utf-8 -*-

class HerramientaIA:
    def __init__(self, nombre: str, version: str):
        self.nombre = nombre
        self.version = version

    def __str__(self):
        return f"HerramientaIA(nombre={self.nombre}, version={self.version})"


