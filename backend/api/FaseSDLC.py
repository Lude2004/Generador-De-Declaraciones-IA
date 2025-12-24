#!/usr/bin/python
#-*- coding: utf-8 -*-

from enum import Enum

class FaseSDLC(Enum):
    PLANIFICACION = "Planificación"
    DISENO = "Análisis"
    IMPLEMENTACION = "Implementación"
    PRUEBAS = "Pruebas"
    DESPLIEGUE = "Despliegue"
    MANTENIMIENTO = "Mantenimiento"
