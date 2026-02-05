#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from domain.metodologia.metodologia import MetodologiaContexto
from core.models import Metodologia, Fase, Tarea

# Verificar si hay metodologías en BD
metodologias = Metodologia.objects.all()
print(f"\nMetodologías en BD: {list(metodologias.values_list('nombre', flat=True))}")

if metodologias.exists():
    nombre_metodo = metodologias.first().nombre
    print(f"\nProbando con: {nombre_metodo}")
    
    try:
        contexto = MetodologiaContexto(nombre_metodo)
        print(f"✓ MetodologiaContexto creado")
        print(f"  Nombre estrategia: {contexto.obtener_nombre()}")
        
        fases = contexto.obtener_fases()
        print(f"\n✓ Fases obtenidas: {len(fases)} fases")
        
        for i, fase in enumerate(fases):
            print(f"\n  Fase {i+1}: {fase.get('nombre', 'SIN NOMBRE')}")
            tareas = fase.get('tareas', [])
            print(f"    - {len(tareas)} tareas")
            if tareas:
                for tarea in tareas[:2]:
                    print(f"      * {tarea.get('nombre', 'sin nombre')}")
        
        print("\n✓ API response simulation:")
        data = {
            "metodologia": contexto.obtener_nombre(),
            "fases": contexto.obtener_fases()
        }
        print(f"  Keys: {data.keys()}")
        print(f"  Fases count: {len(data['fases'])}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("No hay metodologías en la BD")
