from .declaracion_ia_concrete_builder import DeclaracionIAConcreteBuilder
from datetime import date
from typing import Dict, Any


class DeclaracionIADirector:
    """
    Director que orquesta la construcción de declaraciones.
    Implementa el patrón Builder.
    """
    
    def __init__(self):
        self._builder = None

    def set_builder(self, builder: DeclaracionIAConcreteBuilder) -> None:
        """Establece el builder a usar"""
        self._builder = builder

    def construir_declaracion(self, proyecto_data: Dict[str, Any], tareas_data: Dict[str, Any]) -> str:
        """
        Orquesta la construcción completa de una declaración.
        Patrón Builder: cada paso debe ejecutarse en orden específico.
        """
        if not self._builder:
            self._builder = DeclaracionIAConcreteBuilder()
        
        # Pasos del builder en orden
        self._builder.reset()
        self._builder.set_fecha_emision(date.today())
        self._builder.set_proyecto(proyecto_data)
        self._builder.set_equipo(proyecto_data.get('miembros', []))
        self._builder.set_metodologia(proyecto_data.get('metodologia', 'No definida'))
        self._builder.procesar_fases_tareas(tareas_data)
        self._builder.identificar_uso_ia()
        self._builder.set_formato_salida("TEXTO")
        
        # Retorna la declaración construida
        return self._builder.get_resultado()