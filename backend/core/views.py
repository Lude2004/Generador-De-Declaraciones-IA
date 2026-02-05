from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Metodologia, Fase, Tarea
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import date
# Importar desde domain - Patrón Builder
from domain.declaracion.declaracion_ia_director import DeclaracionIADirector
from domain.declaracion.declaracion_ia_concrete_builder import DeclaracionIAConcreteBuilder
# Importar desde domain - Patrón Strategy
from domain.metodologia.metodologia import MetodologiaContexto
# Importar desde domain - Patrón Composite
from domain.tareas.tareas_service import TareasService

def listar_nombres_metodologias(request):
    # Obtenemos solo los nombres de todas las metodologías
    nombres = Metodologia.objects.all().values_list('nombre', flat=True)
    # Convertimos a lista para enviarlo como JSON
    return JsonResponse(list(nombres), safe=False) 


# Nota que ahora recibimos 'nombre_metodo' como argumento extra
def obtener_metodologia(request, nombre_metodo):
    """
    Obtiene la estructura de una metodología.
    Usa el patrón Strategy desde domain/metodologia
    """
    try:
        # Usar Strategy Pattern para obtener la estrategia correcta
        contexto = MetodologiaContexto(nombre_metodo)
        
        # El contexto automáticamente delega a la estrategia correcta
        data = {
            "metodologia": contexto.obtener_nombre(),
            "fases": contexto.obtener_fases()
        }
        
        return JsonResponse(data)

    except ValueError as e:
        return JsonResponse({
            "error": str(e)
        }, status=404)
    except Exception as e:
        return JsonResponse({
            "error": f"Error al obtener metodología: {str(e)}"
        }, status=500)


@require_http_methods(["POST"])
def generar_declaracion(request):
    """
    Genera el texto de la declaración de IA.
    Usa el patrón Builder desde domain/
    """
    try:
        data = json.loads(request.body)
        proyecto_data = data.get('proyecto', {})
        tareas_data = data.get('tareas', {})

        # Usar el Builder Pattern desde domain
        director = DeclaracionIADirector()
        builder = DeclaracionIAConcreteBuilder()
        director.set_builder(builder)
        
        # El director orquesta la construcción
        texto_declaracion = director.construir_declaracion(proyecto_data, tareas_data)

        return JsonResponse({
            'texto_declaracion': texto_declaracion
        })

    except Exception as e:
        return JsonResponse({
            'error': f'Error al generar declaración: {str(e)}'
        }, status=400)



@require_http_methods(["POST"])
def descargar_pdf(request):
    """
    Genera y descarga la declaración en formato PDF.
    Reutiliza el Builder desde domain/
    """
    try:
        data = json.loads(request.body)
        proyecto_data = data.get('proyecto', {})
        tareas_data = data.get('tareas', {})
        nombre_proyecto = proyecto_data.get('nombreProyecto', 'Declaracion_IA')
        
        # Usar el Builder Pattern para generar el texto
        director = DeclaracionIADirector()
        builder = DeclaracionIAConcreteBuilder()
        director.set_builder(builder)
        texto_declaracion = director.construir_declaracion(proyecto_data, tareas_data)
        
        # Crear PDF a partir del texto
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Estilos
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=11,
            textColor='#1a1a1a',
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        )
        
        body_style = ParagraphStyle(
            'CustomBody',
            parent=styles['BodyText'],
            fontSize=10,
            leading=14,
            alignment=4  # Justified
        )
        
        # Agregar contenido al PDF
        for linea in texto_declaracion.split("\n"):
            if linea.strip():
                if linea.isupper() and len(linea) > 3:
                    elements.append(Paragraph(linea, heading_style))
                else:
                    elements.append(Paragraph(linea, body_style))
                elements.append(Spacer(1, 0.08*inch))
            else:
                elements.append(Spacer(1, 0.1*inch))
        
        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        
        # Retornar como descarga
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Declaracion_IA_{nombre_proyecto}.pdf"'
        return response

    except Exception as e:
        return JsonResponse({
            'error': f'Error al generar PDF: {str(e)}'
        }, status=400)