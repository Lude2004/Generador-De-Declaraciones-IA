#-*- coding: utf-8 -*-

class Persona:
    def __init__(self, nombre: str, apellido: str, rol: str):
        self.nombre = nombre
        self.apellido = apellido
        self.rol = rol

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol}"