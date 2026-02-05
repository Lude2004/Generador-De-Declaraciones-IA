#!/usr/bin/python
#-*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import List, TYPE_CHECKING, Dict, Any

if TYPE_CHECKING:
    from domain.tareas import Fase

class MetodologiaStrategy(ABC):
    @abstractmethod
    def obtener_fases(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def obtener_nombre(self) -> str:
        pass