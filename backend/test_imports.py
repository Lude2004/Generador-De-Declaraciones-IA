#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

# Now test all imports
try:
    from domain.tareas.tarea import Tarea
    print("✓ Tarea imports OK")
except Exception as e:
    print(f"✗ Tarea import failed: {e}")

try:
    from domain.entidades import Persona, ProyectoSoftware
    print("✓ Entidades imports OK")
except Exception as e:
    print(f"✗ Entidades import failed: {e}")

try:
    from domain.declaracion.declaracion_ia_director import DeclaracionIADirector
    print("✓ Builder pattern imports OK")
except Exception as e:
    print(f"✗ Builder import failed: {e}")

try:
    from domain.metodologia.metodologia import MetodologiaContexto
    print("✓ Strategy pattern imports OK")
except Exception as e:
    print(f"✗ Strategy import failed: {e}")

try:
    from domain.tareas.tareas_service import TareasService
    print("✓ Composite pattern imports OK")
except Exception as e:
    print(f"✗ Composite import failed: {e}")

try:
    from core.views import generar_declaracion, obtener_metodologia
    print("✓ Views imports OK - ALL PATTERNS WORKING!")
except Exception as e:
    print(f"✗ Views import failed: {e}")
