# -*- coding: utf-8 -*-
"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from core import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/auth/register/', views.register, name='register'),
    path('api/auth/login/', views.login_view, name='login'),
    path('api/auth/me/', views.me, name='me'),
    path('api/auth/logout/', views.logout_view, name='logout'),

    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # URLs con Strategy Pattern REALMENTE FUNCIONAL
    path('api/metodologia/<str:nombre_metodo>', views.obtener_metodologia, name='detalle_metodologia'),
    path('api/lista-metodologias/', views.listar_nombres_metodologias, name='lista_metodologias'),
    
    # URLs con Builder Pattern REALMENTE FUNCIONAL  
    path('api/generar-declaracion/', views.generar_declaracion, name='generar_declaracion'),
    path('api/descargar-pdf/', views.descargar_pdf, name='descargar_pdf'),
    path('api/formatos-disponibles/', lambda request: JsonResponse({'formatos': ['txt', 'pdf']}, safe=False), name='formatos_disponibles'),
    
    # URLs con Composite Pattern para análisis de proyectos
    path('api/analizar-proyecto/', lambda request: JsonResponse({'status': 'Comando de análisis disponible', 'command': 'python manage.py populate_composite_scrum'}, safe=False), name='analizar_proyecto'),
    
    # URL vieja para compatibilidad
    path('api/metodologia/<str:nombre_metodo>', views.obtener_metodologia, name='detalle_metodologia_viejo'),
]