from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
import re
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import date

# REST Framework & JWT
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

# Importar desde domain - Patrón Builder
from domain.declaracion.declaracion_ia_director import DeclaracionIADirector
from domain.declaracion.declaracion_ia_concrete_builder import DeclaracionIAConcreteBuilder
# Importar desde domain - Patrón Strategy
from domain.metodologia.metodologia import MetodologiaContexto
# Importar desde domain - Patrón Composite
from domain.tareas.tareas_service import TareasService

# Models
from .models import Metodologia, Fase, Tarea

def validar_email(email):
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def obtener_datos_usuario(usuario):
    """Retorna datos seguros del usuario (sin contraseña)"""
    return {
        'id': usuario.id,
        'email': usuario.email,
        'nombre': usuario.first_name,
        'apellido': usuario.last_name,
        'username': usuario.username,
    }

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

#Endpoint REGISTRO

# HELPER: Generar tokens
def obtener_tokens_usuario(usuario):
    refresh = RefreshToken.for_user(usuario)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    """Registra un nuevo usuario y retorna tokens JWT"""
    try:
        data = json.loads(request.body)
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        nombre = data.get('nombre', '').strip()
        apellido = data.get('apellido', '').strip()
        
        if not all([email, password, nombre]):
            return JsonResponse({
                'error': 'Email, contraseña y nombre son requeridos'
            }, status=400)
        
        if not validar_email(email):
            return JsonResponse({'error': 'Email inválido'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Este email ya está registrado'}, status=400)
        
        try:
            validate_password(password)
        except ValidationError as e:
            return JsonResponse({
                'error': f'Contraseña débil: {", ".join(e.messages)}'
            }, status=400)
        
        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=nombre,
            last_name=apellido
        )
        
        tokens = obtener_tokens_usuario(usuario)
        
        return JsonResponse({
            'mensaje': 'Usuario registrado exitosamente',
            'usuario': obtener_datos_usuario(usuario),
            'tokens': tokens
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al registrar: {str(e)}'}, status=500)

@require_http_methods(["POST"])
@csrf_exempt
def login_view(request):
    """Inicia sesión y retorna tokens JWT"""
    try:
        data = json.loads(request.body)
        
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        if not email or not password:
            return JsonResponse({
                'error': 'Email y contraseña son requeridos'
            }, status=400)
        
        try:
            usuario = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'Email o contraseña incorrectos'
            }, status=401)
        
        usuario_autenticado = authenticate(
            request, 
            username=usuario.username,
            password=password
        )
        
        if usuario_autenticado is None:
            return JsonResponse({
                'error': 'Email o contraseña incorrectos'
            }, status=401)
        
        tokens = obtener_tokens_usuario(usuario_autenticado)
        
        return JsonResponse({
            'mensaje': 'Sesión iniciada exitosamente',
            'usuario': obtener_datos_usuario(usuario_autenticado),
            'tokens': tokens
        }, status=200)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Error al iniciar sesión: {str(e)}'}, status=500)

@require_http_methods(["GET"])
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    """Obtiene el usuario actual (requiere token JWT)"""
    return Response({
        'usuario': obtener_datos_usuario(request.user)
    }, status=200)

#Endpoint LOGOUT
@require_http_methods(["POST"])
def logout_view(request):
    """
    Cierra la sesión del usuario.
    """
    if not request.user.is_authenticated:
        return JsonResponse({
            'error': 'No hay sesión activa'
        }, status=400)
    
    auth_logout(request)
    
    return JsonResponse({
        'mensaje': 'Sesión cerrada exitosamente'
    }, status=200)