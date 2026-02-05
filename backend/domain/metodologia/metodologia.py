#-*- coding: utf-8 -*-

from .metodologia_strategy import MetodologiaStrategy
from .scrum_strategy import ScrumStrategy
from .xp_strategy import XPStrategy
from core.models import Metodologia as MetodologiaModel, Fase, Tarea
from typing import List, Dict, Any


class MetodologiaContexto:
    """
    Contexto que aplica el patrón Strategy.
    Selecciona automáticamente la estrategia correcta según la metodología.
    """
    
    # Mapeo de names a estrategias
    ESTRATEGIAS = {
        'SCRUM': ScrumStrategy,
        'XP': XPStrategy,
    }
    
    def __init__(self, nombre_metodologia: str):
        self.nombre_metodologia = nombre_metodologia.upper()
        self.estrategia: MetodologiaStrategy = None
        self._inicializar_estrategia()
    
    def _inicializar_estrategia(self) -> None:
        """Inicializa la estrategia correcta según el nombre"""
        try:
            # Buscar metodología en BD
            metodologia_obj = MetodologiaModel.objects.get(nombre__iexact=self.nombre_metodologia)
            
            # Obtener clase de estrategia
            if self.nombre_metodologia in self.ESTRATEGIAS:
                EstrategiaClass = self.ESTRATEGIAS[self.nombre_metodologia]
            else:
                # Usar estrategia genérica si no hay una específica
                EstrategiaClass = self._crear_estrategia_generica()
            
            # Instanciar estrategia
            self.estrategia = EstrategiaClass(metodologia_obj)
            
        except MetodologiaModel.DoesNotExist:
            raise ValueError(f"Metodología '{self.nombre_metodologia}' no encontrada en BD")
    
    def obtener_fases(self) -> List[Dict[str, Any]]:
        """Delega la obtención de fases a la estrategia"""
        if not self.estrategia:
            raise RuntimeError("Estrategia no inicializada")
        return self.estrategia.obtener_fases()
    
    def obtener_nombre(self) -> str:
        """Delega al obtener el nombre a la estrategia"""
        if not self.estrategia:
            raise RuntimeError("Estrategia no inicializada")
        return self.estrategia.obtener_nombre()
    
    def validar_estructura(self) -> bool:
        """Delega la validación a la estrategia"""
        if not self.estrategia:
            raise RuntimeError("Estrategia no inicializada")
        return self.estrategia.validar_estructura()
    
    def _crear_estrategia_generica(self) -> type:
        """
        Crea una estrategia genérica para metodologías no mapeadas específicamente.
        Patrón Strategy: implementación por defecto.
        """
        class EstrategiaGenericaMetodologia(MetodologiaStrategy):
            def __init__(self, metodologia_obj):
                self.metodologia = metodologia_obj
            
            def obtener_fases(self) -> List[Dict[str, Any]]:
                fases = Fase.objects.filter(metodologia=self.metodologia).order_by('id')
                return [
                    {
                        "nombre": fase.nombre,
                        "tareas": [
                            {
                                "nombre": f"tarea-{t.id}",
                                "descripcion": t.descripcion,
                                "categoria": t.categoria,
                                "id": t.id
                            } for t in Tarea.objects.filter(fase=fase).order_by('id')
                        ]
                    } for fase in fases
                ]
            
            def obtener_nombre(self) -> str:
                return self.metodologia.nombre
            
            def validar_estructura(self) -> bool:
                # Validación genérica
                return Fase.objects.filter(metodologia=self.metodologia).count() > 0
        
        return EstrategiaGenericaMetodologia


class Metodologia:
    """Clase original mantenida para compatibilidad"""
    
    def __init__(self, strategy: MetodologiaStrategy):
        self.metodologia = strategy

    def obtener_fases(self) -> List[Fase]:
        return self.metodologia.obtener_fases()

    def obtener_nombre(self) -> str:
        return self.metodologia.obtener_nombre()    
    
    def cambiar_metodologia(self, strategy: MetodologiaStrategy) -> None:
        self.metodologia = strategy