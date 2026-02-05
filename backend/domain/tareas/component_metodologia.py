from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class ComponentMetodologia(ABC):
    """
    Componente abstracto del patrón Composite.
    Define la interfaz para componentes simples (hojas) y compuestos (ramas).
    """
    
    @abstractmethod
    def obtener_nombre(self) -> str:
        """Retorna el nombre del componente"""
        pass
    
    @abstractmethod
    def obtener_descripcion(self) -> str:
        """Retorna la descripción del componente"""
        pass
    
    @abstractmethod
    def mostrar_estructura(self, nivel: int = 0) -> str:
        """Muestra la estructura jerárquica"""
        pass
    
    @abstractmethod
    def obtener_datos(self) -> Dict[str, Any]:
        """Retorna los datos del componente"""
        pass


class TareaHoja(ComponentMetodologia):
    """
    Hoja (Leaf) del patrón Composite.
    Representa una tarea individual sin sub-componentes.
    """
    
    def __init__(self, nombre: str, descripcion: str, categoria: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.categoria = categoria
    
    def obtener_nombre(self) -> str:
        return self.nombre
    
    def obtener_descripcion(self) -> str:
        return self.descripcion
    
    def mostrar_estructura(self, nivel: int = 0) -> str:
        """Muestra la tarea individual"""
        indent = "  " * nivel
        return f"{indent}• {self.nombre} ({self.categoria})"
    
    def obtener_datos(self) -> Dict[str, Any]:
        """Retorna los datos de la tarea"""
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "categoria": self.categoria,
            "tipo": "tarea"
        }


class FaseCompuesta(ComponentMetodologia):
    """
    Rama (Composite) del patrón Composite.
    Representa una fase que contiene múltiples tareas (hojas) o sub-fases.
    """
    
    def __init__(self, nombre: str, descripcion: str = ""):
        self.nombre = nombre
        self.descripcion = descripcion
        self.componentes: List[ComponentMetodologia] = []
    
    def agregar_componente(self, componente: ComponentMetodologia) -> None:
        """Agrega un componente (tarea o sub-fase) a esta fase"""
        self.componentes.append(componente)
    
    def remover_componente(self, componente: ComponentMetodologia) -> None:
        """Remueve un componente"""
        self.componentes.remove(componente)
    
    def obtener_nombre(self) -> str:
        return self.nombre
    
    def obtener_descripcion(self) -> str:
        return self.descripcion
    
    def mostrar_estructura(self, nivel: int = 0) -> str:
        """
        Muestra la estructura jerárquica de la fase y sus componentes.
        Recursivo: muestra todas las sub-fases y tareas.
        """
        indent = "  " * nivel
        resultado = f"{indent}📁 {self.nombre}\n"
        
        for componente in self.componentes:
            resultado += componente.mostrar_estructura(nivel + 1) + "\n"
        
        return resultado.rstrip()
    
    def obtener_datos(self) -> Dict[str, Any]:
        """
        Retorna los datos de la fase y todos sus componentes.
        Recursivo: construye la estructura completa.
        """
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "tipo": "fase",
            "componentes": [componente.obtener_datos() for componente in self.componentes]
        }
    
    def obtener_todas_tareas(self) -> List[TareaHoja]:
        """
        Retorna TODAS las tareas (hojas) de esta fase y sub-fases.
        Recursivo.
        """
        tareas = []
        for componente in self.componentes:
            if isinstance(componente, TareaHoja):
                tareas.append(componente)
            elif isinstance(componente, FaseCompuesta):
                tareas.extend(componente.obtener_todas_tareas())
        return tareas
    
    def contar_tareas(self) -> int:
        """Cuenta todas las tareas en esta fase y sub-fases"""
        return len(self.obtener_todas_tareas())
    
    def contar_fases(self) -> int:
        """Cuenta todas las fases (incluyendo sub-fases)"""
        count = 1
        for componente in self.componentes:
            if isinstance(componente, FaseCompuesta):
                count += componente.contar_fases()
        return count


class ConstructorMetodologia:
    """
    Constructor que facilita la creación de estructuras Composite.
    Toma datos de BD y construye el árbol de componentes.
    """
    
    @staticmethod
    def construir_desde_bd(metodologia_obj, fases_queryset, tareas_queryset) -> FaseCompuesta:
        """
        Construye la estructura Composite desde datos de BD.
        
        Args:
            metodologia_obj: Objeto Metodología de Django
            fases_queryset: QuerySet de Fases
            tareas_queryset: QuerySet de Tareas
        
        Returns:
            FaseCompuesta: Raíz del árbol Composite
        """
        # Crear fase raíz (metodología)
        raiz = FaseCompuesta(metodologia_obj.nombre, f"Metodología {metodologia_obj.nombre}")
        
        # Agregar cada fase como sub-rama
        for fase in fases_queryset:
            fase_compuesta = FaseCompuesta(fase.nombre, fase.nombre)
            
            # Agregar tareas a la fase
            tareas_de_fase = tareas_queryset.filter(fase=fase)
            for tarea in tareas_de_fase:
                tarea_hoja = TareaHoja(tarea.descripcion, tarea.descripcion, tarea.categoria)
                fase_compuesta.agregar_componente(tarea_hoja)
            
            raiz.agregar_componente(fase_compuesta)
        
        return raiz
    
    @staticmethod
    def convertir_a_dict_tareas(estructura_compuesta: FaseCompuesta) -> Dict[str, Any]:
        """
        Convierte la estructura Composite a diccionario compatible con el frontend.
        """
        fases_dict = []
        
        for componente in estructura_compuesta.componentes:
            if isinstance(componente, FaseCompuesta):
                fase_dict = {
                    "nombre": componente.nombre,
                    "tareas": [
                        {
                            "nombre": tarea.nombre,
                            "descripcion": tarea.descripcion,
                            "categoria": tarea.categoria
                        } for tarea in componente.obtener_todas_tareas()
                    ]
                }
                fases_dict.append(fase_dict)
        
        return {
            "metodologia": estructura_compuesta.nombre,
            "fases": fases_dict
        }