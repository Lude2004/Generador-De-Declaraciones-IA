#-*- coding: utf-8 -*-

class UsoIA:
    def __init__(self, nombre: str, version: str, justificacion: str):
        self.nombreHerramientaIA = nombre
        self.versionHerramientaIA = version
        self.justificacion = justificacion

    def __str__(self):
        return f"HerramientaIA(nombre={self.nombreHerramientaIA}, version={self.versionHerramientaIA}, justificacion={self.justificacion})"