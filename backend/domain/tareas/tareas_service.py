"""
Servicio de Tareas - Usa el patrón Composite.
Obtiene la estructura jerárquica de tareas desde la BD.
"""

from .component_metodologia import FaseCompuesta, TareaHoja, ConstructorMetodologia
from core.models import Metodologia, Fase, Tarea
from typing import Dict, Any


class TareasService:
    """
    Servicio que usa el patrón Composite para gestionar tareas.
    Las tareas se organizan jerárquicamente en fases.
    """
    
    @staticmethod
    def obtener_estructura_tareas(metodologia_nombre: str) -> Dict[str, Any]:
        """
        Obtiene las tareas organizadas en una estructura Composite.
        
        Patrón Composite: 
        - Fase es una rama (Composite)
        - Tarea es una hoja (Leaf)
        - Se pueden navegar recursivamente
        """
        try:
            # Obtener metodología
            metodologia = Metodologia.objects.get(nombre__iexact=metodologia_nombre)
            
            # Obtener fases y tareas
            fases = Fase.objects.filter(metodologia=metodologia).order_by('id')
            tareas = Tarea.objects.filter(fase__in=fases)
            
            # Construir estructura Composite
            estructura = ConstructorMetodologia.construir_desde_bd(
                metodologia, 
                fases, 
                tareas
            )
            
            # Convertir a diccionario para respuesta
            return ConstructorMetodologia.convertir_a_dict_tareas(estructura)
        
        except Metodologia.DoesNotExist:
            raise ValueError(f"Metodología '{metodologia_nombre}' no encontrada")
    
    @staticmethod
    def mostrar_estructura_visual(metodologia_nombre: str) -> str:
        """
        Muestra la estructura de tareas de forma visual (árbol).
        Útil para debugging y visualización.
        """
        try:
            metodologia = Metodologia.objects.get(nombre__iexact=metodologia_nombre)
            fases = Fase.objects.filter(metodologia=metodologia).order_by('id')
            tareas = Tarea.objects.filter(fase__in=fases)
            
            estructura = ConstructorMetodologia.construir_desde_bd(
                metodologia, 
                fases, 
                tareas
            )
            
            return estructura.mostrar_estructura()
        
        except Metodologia.DoesNotExist:
            return f"Metodología '{metodologia_nombre}' no encontrada"
    
    @staticmethod
    def contar_tareas(metodologia_nombre: str) -> int:
        """Cuenta el total de tareas usando el Composite"""
        try:
            metodologia = Metodologia.objects.get(nombre__iexact=metodologia_nombre)
            fases = Fase.objects.filter(metodologia=metodologia).order_by('id')
            tareas = Tarea.objects.filter(fase__in=fases)
            
            estructura = ConstructorMetodologia.construir_desde_bd(
                metodologia, 
                fases, 
                tareas
            )
            
            return estructura.contar_tareas()
        
        except:
            return 0
