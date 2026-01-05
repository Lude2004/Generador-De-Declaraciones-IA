#-*- coding: utf-8 -*-

from datetime import datetime
from .proyectosoftware import ProyectoSoftware

class DeclaracionIA:
    def __init__(self, proyecto: ProyectoSoftware):
        self.fecha_emision = datetime.now()
        self.proyecto = proyecto

    def generar_texto_declaracion(self) -> str:
        nombre_proyecto = self.proyecto.nombre
        fecha_actual = self.fecha_emision.strftime("%d de %B de %Y")
        metodologia_nombre = self.proyecto.metodologia.nombre if self.proyecto.metodologia else "No definida"
        miembros = self.proyecto.equipo.miembros if self.proyecto.equipo else []

        # 1. ENCABEZADO FORMAL
        texto = "DECLARACIÓN DE USO DE INTELIGENCIA ARTIFICIAL GENERATIVA\n\n"
        texto += f"Fecha: {fecha_actual}\n\n"

        # 2. PÁRRAFO INTRODUCTORIO
        texto += (
            f"El equipo de desarrollo declara que las herramientas de inteligencia artificial "
            f"generativa especificadas en este documento fueron utilizadas como apoyo en las "
            f"tareas indicadas de la metodología {metodologia_nombre} durante el desarrollo del proyecto \"{nombre_proyecto}\".\n\n"
        )

        # 3. TAREAS DELEGADAS A IA CON SUPERVISIÓN HUMANA
        tareas_con_ia = False
        if self.proyecto.metodologia:
            for fase in self.proyecto.metodologia.obtener_fases():
                tareas_fase = [t for t in fase.obtener_tareas() if t.seleccionada]
                
                if tareas_fase:
                    tareas_con_ia = True
                    texto += f"Fase: {fase.nombre}\n"
                    
                    for tarea in tareas_fase:
                        herramienta = tarea.herramienta_ia.nombre if tarea.herramienta_ia else "No especificada"
                        version = f" (versión {tarea.herramienta_ia.version})" if tarea.herramienta_ia and tarea.herramienta_ia.version else ""
                        
                        texto += f"   • {tarea.nombre} - Asistida por {herramienta}{version}.\n"
                    
                    texto += "\n"
        
        if not tareas_con_ia:
            texto += "  (No se registraron tareas asistidas por IA en esta sesión)\n\n"

        # 4. GARANTÍAS DE CALIDAD Y SUPERVISIÓN
        texto += (
            "Todas las salidas generadas por IA fueron revisadas, validadas y, cuando fue necesario, "
            "modificadas por los miembros del equipo para asegurar su calidad, precisión y "
            "alineación con los objetivos del proyecto.\n"
        )

        # 5. RESPONSABILIDAD Y AUTORÍA
        texto += (
            "La responsabilidad del contenido final recae íntegramente en los miembro del equipo de desarrollo.\n"
        )
        texto += (
            "Las herramientas de IA generativa no figuran como autores y no asumen responsabilidad "
            "alguna por los resultados finales.\n"
        )
        
        return texto

    def generar_pdf(self):
        # Lógica futura para PDF
        pass