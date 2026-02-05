from .declaracion_ia import DeclaracionIA
from abc import ABC, abstractmethod
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from domain.entidades import Equipo, ProyectoSoftware
    from domain.metodologia import Metodologia

class DeclaracionIABuilder(ABC):
    @abstractmethod
    def reset(self) -> None: pass
    
    @abstractmethod
    def set_fecha_emision(self, fecha: date) -> None: pass
    
    @abstractmethod
    def set_proyecto(self, proyecto: 'ProyectoSoftware') -> None: pass
    
    @abstractmethod
    def set_equipo(self, equipo: 'Equipo') -> None: pass
    
    @abstractmethod
    def set_metodologia(self, metodologia: 'Metodologia') -> None: pass
    
    @abstractmethod
    def procesar_fases_tareas(self) -> None: pass
    
    @abstractmethod
    def identificar_uso_ia(self) -> None: pass
    
    @abstractmethod
    def set_formato_salida(self, formato: str) -> None: pass
    
    @abstractmethod
    def get_resultado(self) -> DeclaracionIA: pass