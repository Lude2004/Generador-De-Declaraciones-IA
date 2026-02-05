from .metodologia_strategy import MetodologiaStrategy
from core.models import Metodologia, Fase, Tarea
from typing import List, Dict, Any


class XPStrategy(MetodologiaStrategy):
    """Estrategia concreta para XP (Extreme Programming)"""
    
    def __init__(self, metodologia_obj):
        self.metodologia = metodologia_obj
    
    def obtener_fases(self) -> List[Dict[str, Any]]:
        """Obtiene las fases de XP desde la BD"""
        fases = Fase.objects.filter(metodologia=self.metodologia).order_by('id')
        return [self._construir_fase(fase) for fase in fases]
    
    def obtener_nombre(self) -> str:
        """Retorna el nombre de la metodología"""
        return self.metodologia.nombre
    
    def validar_estructura(self) -> bool:
        """
        Validación específica XP.
        XP requiere al menos 1 fase (iteraciones cortas)
        """
        fases = Fase.objects.filter(metodologia=self.metodologia)
        return fases.count() >= 1
    
    def _construir_fase(self, fase: Fase) -> Dict[str, Any]:
        """Construye la estructura de una fase con sus tareas"""
        tareas = Tarea.objects.filter(fase=fase).order_by('id')
        return {
            "nombre": fase.nombre,
            "tareas": [
                {
                    "nombre": f"tarea-{tarea.id}",
                    "descripcion": tarea.descripcion,
                    "categoria": tarea.categoria,
                    "id": tarea.id
                } for tarea in tareas
            ]
        }