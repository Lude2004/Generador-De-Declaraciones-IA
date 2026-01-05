from django.http import JsonResponse
from .proyectosoftware import ProyectoSoftware
from .persona import Persona
from .declaracionia import DeclaracionIA
from .metodologia import Metodologia
from .MetodologiaAgil import MetodologiaAgil 
from .fase import Fase
from .tarea import Tarea
from .herramientaia import HerramientaIA
import json

from django.views.decorators.csrf import csrf_exempt

def fabricar_estructura(nombre_metodologia):
    print(f"--- GENERANDO DATOS PARA: {nombre_metodologia} ---") # Debug

    # ==========================================
    #                 SCRUM
    # ==========================================
    if nombre_metodologia == MetodologiaAgil.SCRUM.value:
        metodo = Metodologia(MetodologiaAgil.SCRUM)
        
        # 1. PREGAME: PLANNING
        fase_planning = Fase("Pregame: Planning")
        t_plan = [
            "Definición de un nuevo release basado en el backlog conocido",
            "Estimación del cronograma del proyecto",
            "Estimación de costos del proyecto",
            "Conceptualización del sistema (si es un sistema nuevo)",
            "Análisis del sistema (completo o limitado según el caso)"
        ]
        for t in t_plan:
            fase_planning.agregar_tarea(Tarea(t, "Planificación"))
        metodo.agregar_fase(fase_planning)

        # 2. PREGAME: ARCHITECTURE
        fase_arch = Fase("Pregame: Architecture")
        t_arch = [
            "Diseño de la implementación de los ítems del backlog",
            "Diseño de alto nivel del sistema",
            "Modificación de la arquitectura del sistema"
        ]
        for t in t_arch:
            fase_arch.agregar_tarea(Tarea(t, "Arquitectura"))
        metodo.agregar_fase(fase_arch)

        # 3. GAME: DEVELOPMENT
        fase_game = Fase("Game: Development Sprints")
        t_game = [
            "Desarrollo de funcionalidades del nuevo release",
            "Ejecución de sprints iterativos",
            "Gestión continua del tiempo",
            "Gestión de requisitos",
            "Control de calidad",
            "Control de costos",
            "Adaptación a la competencia y cambios"
        ]
        for t in t_game:
            fase_game.agregar_tarea(Tarea(t, "Desarrollo"))
        metodo.agregar_fase(fase_game)

        # 4. POSTGAME: CLOSURE
        fase_post = Fase("Postgame: Closure")
        t_post = [
            "Preparación del producto para liberación",
            "Elaboración de documentación final",
            "Pruebas previas a la liberación (staged testing)",
            "Liberación del producto"
        ]
        for t in t_post:
            fase_post.agregar_tarea(Tarea(t, "Cierre"))
        metodo.agregar_fase(fase_post)

        return metodo

    # ==========================================
    #       EXTREME PROGRAMMING (XP) - ¡NUEVO!
    # ==========================================
    elif nombre_metodologia == MetodologiaAgil.XP.value:
        metodo = Metodologia(MetodologiaAgil.XP)
        
        # 1. EXPLORACIÓN
        fase_exploracion = Fase("Exploración")
        t_exploracion = [
            "Definición de requisitos",
            "Descripción del diseño",
            "Descripción de la arquitectura del cliente",
            "Descripción de las herramientas y el software utilizado",
            "Creación de historias de usuario completas y detalladas",
            "Estimación de tiempos"
        ]
        for t in t_exploracion:
            fase_exploracion.agregar_tarea(Tarea(t, "Análisis Inicial"))
        metodo.agregar_fase(fase_exploracion)

        # 2. PLANIFICACIÓN
        fase_plan = Fase("Planificación")
        fase_plan.agregar_tarea(Tarea("Creación de tarjetas de tareas", "Gestión"))
        metodo.agregar_fase(fase_plan)

        # 3. ITERACIÓN A LANZAMIENTO
        fase_iteracion = Fase("Iteración a Lanzamiento")
        t_iteracion = [
            "Diseño",
            "Codificación",
            "Pruebas unitarias y funcionales",
            "Refactorización del código"
        ]
        for t in t_iteracion:
            fase_iteracion.agregar_tarea(Tarea(t, "Ingeniería"))
        metodo.agregar_fase(fase_iteracion)

        # 4. PRODUCCIÓN
        fase_prod = Fase("Producción")
        t_prod = [
            "Entrega de pequeñas versiones",
            "Ciclos de retroalimentación rápidos",
            "Monitoreo del sistema"
        ]
        for t in t_prod:
            fase_prod.agregar_tarea(Tarea(t, "Despliegue"))
        metodo.agregar_fase(fase_prod)

        # 5. MANTENIMIENTO
        fase_mant = Fase("Mantenimiento")
        t_mant = [
            "Actualización del software",
            "Desarrollo de nuevas funcionalidades",
            "Eliminación de las modificaciones"
        ]
        for t in t_mant:
            fase_mant.agregar_tarea(Tarea(t, "Soporte"))
        metodo.agregar_fase(fase_mant)

        # 6. MUERTE (CIERRE)
        fase_muerte = Fase("Muerte (Cierre del Proyecto)")
        t_muerte = [
            "Verificación de todos los requisitos",
            "Redacción de la documentación necesaria del sistema"
        ]
        for t in t_muerte:
            fase_muerte.agregar_tarea(Tarea(t, "Documentación Final"))
        metodo.agregar_fase(fase_muerte)

        return metodo
    
    return None

def listar_metodologias(request):
    """Devuelve ['Scrum', 'Extreme Programming'] para el dropdown"""
    opciones = [m.value for m in MetodologiaAgil]
    return JsonResponse(opciones, safe=False)

def obtener_detalles_metodologia(request):
    """
    Convierte tus objetos (Clases) a JSON (Diccionarios)
    """
    nombre = request.GET.get("nombre")

    # 1. Llamamos a la fábrica para obtener los datos NUEVOS
    metodologia = fabricar_estructura(nombre)
    
    if not metodologia:
        return JsonResponse({"error": "Metodología no encontrada"}, status=404)

    # AQUÍ ESTABA EL ERROR: Borré la línea que decía "metodologia = PROYECTO_DEMO"
    
    datos = {
        "nombre": metodologia.nombre,
        "fases": []
    }

    for fase in metodologia.obtener_fases():
        fase_dict = {
            "nombre": fase.nombre,
            "tareas": []
        }
        for tarea in fase.obtener_tareas():
            fase_dict["tareas"].append({
                "nombre": tarea.nombre,
                "descripcion": tarea.descripcion,
                "seleccionada": tarea.seleccionada
            })
        datos["fases"].append(fase_dict)

    return JsonResponse(datos)

@csrf_exempt
def generar_declaracion(request):
    """Genera la declaración de uso de IA"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"DEBUG - Datos recibidos: {data}")
            
            proyecto_data = data.get('proyecto', {})
            tareas_data = data.get('tareas', {})
            
            print(f"DEBUG - Proyecto data: {proyecto_data}")
            print(f"DEBUG - Tareas data: {tareas_data}")
            
            # 1. Crear proyecto
            proyecto = ProyectoSoftware(proyecto_data.get('nombreProyecto', 'Sin nombre'))
            print(f"DEBUG - Proyecto creado: {proyecto.nombre}")
            
            # 2. Agregar miembros del equipo
            for miembro in proyecto_data.get('miembros', []):
                persona = Persona(
                    miembro.get('nombre', ''),
                    miembro.get('apellido', ''),
                    miembro.get('rol', '')
                )
                proyecto.equipo.agregar_miembro(persona)
                print(f"DEBUG - Miembro agregado: {persona.nombre}")
            
            # 3. Obtener y asignar metodología
            metodologia_nombre = proyecto_data.get('metodologia', '')
            print(f"DEBUG - Metodología seleccionada: {metodologia_nombre}")
            
            metodologia = fabricar_estructura(metodologia_nombre)
            if metodologia:
                proyecto.seguir_metodologia(metodologia)
                print(f"DEBUG - Metodología asignada")
                
                # 4. Marcar tareas seleccionadas y asignar herramientas
                for fase in metodologia.obtener_fases():
                    for tarea in fase.obtener_tareas():
                        if tarea.nombre in tareas_data:
                            tarea_info = tareas_data[tarea.nombre]
                            if tarea_info.get('seleccionada'):
                                tarea.seleccionada = True
                                herramienta = HerramientaIA(
                                    tarea_info.get('herramienta', 'Desconocida'),
                                    tarea_info.get('version', '1.0')
                                )
                                tarea.herramienta_ia = herramienta
                                print(f"DEBUG - Tarea marcada: {tarea.nombre}")
            else:
                print(f"DEBUG - ERROR: Metodología no encontrada")
            
            # 5. Generar declaración
            print(f"DEBUG - Generando declaración...")
            declaracion = DeclaracionIA(proyecto)
            texto = declaracion.generar_texto_declaracion()
            print(f"DEBUG - Declaración generada exitosamente")
            
            return JsonResponse({"texto_declaracion": texto})
            
        except Exception as e:
            import traceback
            error_msg = traceback.format_exc()
            print(f"ERROR COMPLETO:\n{error_msg}")
            return JsonResponse({"error": str(e)}, status=400)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)