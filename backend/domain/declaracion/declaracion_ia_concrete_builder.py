from .declaracion_ia_builder import DeclaracionIABuilder
from .declaracion_ia import DeclaracionIA
from typing import Optional, List, Dict, Any
from datetime import date


class DeclaracionIAConcreteBuilder(DeclaracionIABuilder):
    """Builder concreto para declaraciones de IA con datos reales"""
    
    def __init__(self):
        self._declaracion = DeclaracionIA()
        self._proyecto: Optional[Dict[str, Any]] = None
        self._tareas: Optional[Dict[str, Any]] = None
        self._miembros: List[Dict[str, Any]] = []

    def reset(self) -> None:
        """Reinicia el builder"""
        self._declaracion = DeclaracionIA()

    def set_fecha_emision(self, fecha: date) -> None:
        """Establece la fecha de emisión"""
        self._declaracion.fecha_emision = fecha

    def set_proyecto(self, proyecto: Dict[str, Any]) -> None:
        """Establece los datos del proyecto"""
        self._proyecto = proyecto
        self._miembros = proyecto.get('miembros', [])

    def set_equipo(self, miembros: List[Dict[str, Any]]) -> None:
        """Establece el equipo"""
        self._miembros = miembros

    def set_metodologia(self, metodologia: str) -> None:
        """Establece la metodología"""
        self._metodologia_nombre = metodologia

    def procesar_fases_tareas(self, tareas_data: Dict[str, Any]) -> None:
        """Procesa las tareas seleccionadas y las agrupa por fase"""
        self._tareas = tareas_data

    def identificar_uso_ia(self) -> None:
        """Identificar el uso de IA (parte del builder)"""
        pass

    def set_formato_salida(self, formato: str) -> None:
        """Establece el formato de salida"""
        self._formato = formato

    def get_resultado(self) -> str:
        """
        Retorna la declaración construida como texto.
        Este es el método que ejecuta el patrón Builder.
        """
        contenido = []
        
        # 1. ENCABEZADO
        contenido.append("DECLARACIÓN DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA")
        contenido.append("")
        fecha_formateada = self._declaracion.fecha_emision.strftime("%d de %B de %Y")
        contenido.append(f"Fecha: {fecha_formateada}")
        contenido.append("")
        
        # 2. INTRODUCCIÓN
        nombre_proyecto = self._proyecto.get('nombreProyecto', 'Sin especificar')
        metodologia = self._proyecto.get('metodologia', 'No definida')
        
        if len(self._miembros) == 1:
            miembro = self._miembros[0]
            contenido.append(
                f"{miembro.get('nombre', '')} {miembro.get('apellido', '')} ({miembro.get('rol', '')}) declara que las herramientas de inteligencia artificial "
                f"generativa especificadas en este documento fueron utilizadas como apoyo en las "
                f"tareas indicadas de la metodología {metodologia} durante el desarrollo del proyecto \"{nombre_proyecto}\"."
            )
        else:
            nombres_miembros = ", ".join([f"{m.get('nombre', '')} {m.get('apellido', '')} ({m.get('rol', '')})" for m in self._miembros])
            contenido.append(
                f"El equipo de desarrollo conformado por {nombres_miembros} declara que las herramientas de inteligencia artificial "
                f"generativa especificadas en este documento fueron utilizadas como apoyo en las "
                f"tareas indicadas de la metodología {metodologia} durante el desarrollo del proyecto \"{nombre_proyecto}\"."
            )
        
        contenido.append("")
        
        # 3. TAREAS AGRUPADAS POR FASE
        tareas_utilizadas = []
        for nombre_tarea, datos_tarea in self._tareas.items():
            if datos_tarea.get('seleccionada'):
                tareas_utilizadas.append({
                    'tarea': nombre_tarea,
                    'descripcion': datos_tarea.get('descripcion', nombre_tarea),
                    'herramienta': datos_tarea.get('herramienta', ''),
                    'version': datos_tarea.get('version', ''),
                    'responsable': datos_tarea.get('responsable', ''),
                    'fase': datos_tarea.get('fase', '')
                })
        
        if tareas_utilizadas:
            # Agrupar por fase
            tareas_por_fase = {}
            for tarea_info in tareas_utilizadas:
                fase = tarea_info['fase'] or 'Sin fase especificada'
                if fase not in tareas_por_fase:
                    tareas_por_fase[fase] = []
                tareas_por_fase[fase].append(tarea_info)
            
            contenido.append("TAREAS ASISTIDAS POR INTELIGENCIA ARTIFICIAL GENERATIVA:")
            contenido.append("")
            
            mostrar_responsable = len(self._miembros) > 1
            
            for fase, tareas in tareas_por_fase.items():
                contenido.append(f"En la Fase: {fase}")
                for tarea_info in tareas:
                    herramienta = tarea_info['herramienta']
                    version = f" (versión {tarea_info['version']})" if tarea_info['version'] else ""
                    descripcion_tarea = tarea_info.get('descripcion', tarea_info.get('tarea', 'Tarea sin especificar'))
                    linea = f"   • {descripcion_tarea} - Asistida por {herramienta}{version}."
                    
                    if mostrar_responsable and tarea_info['responsable']:
                        linea += f" Responsable: {tarea_info['responsable']}."
                    
                    contenido.append(linea)
                contenido.append("")
        
        # 4. GARANTÍAS
        contenido.append("")
        if len(self._miembros) == 1:
            contenido.append(
                "Todas las salidas generadas por IA fueron revisadas, validadas y, cuando fue necesario, "
                "modificadas por el autor para asegurar su calidad, precisión y "
                "alineación con los objetivos del proyecto."
            )
        else:
            contenido.append(
                "Todas las salidas generadas por IA fueron revisadas, validadas y, cuando fue necesario, "
                "modificadas por los miembros del equipo para asegurar su calidad, precisión y "
                "alineación con los objetivos del proyecto."
            )
        
        contenido.append("")
        
        # 5. RESPONSABILIDAD
        contenido.append("")
        if len(self._miembros) == 1:
            contenido.append("La responsabilidad del contenido final recae íntegramente en el autor.")
        else:
            contenido.append("La responsabilidad del contenido final recae íntegramente en los miembros del equipo de desarrollo.")
        
        contenido.append("")
        contenido.append(
            "Las herramientas de IA generativa no figuran como autores y no asumen responsabilidad "
            "alguna por los resultados finales."
        )
        
        contenido.append("")
        contenido.append("=" * 80)
        
        return "\n".join(contenido)