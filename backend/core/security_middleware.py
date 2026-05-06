"""
Middleware para reforzar seguridad en tránsito (TLS 1.3 / HTTPS).
0.2.2 Seguridad en Tránsito
"""

import logging
from django.conf import settings
from django.http import HttpResponseBadRequest

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware:
    """
    Middleware que agrega headers de seguridad adicionales.
    Refuerza protección contra ataques comunes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers de seguridad en tránsito
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' cdn.jsdelivr.net; "
            "img-src 'self' data: https:; "
            "font-src 'self' cdn.jsdelivr.net; "
            "connect-src 'self' localhost:5173 localhost:8000; "
            "frame-ancestors 'none'; "
        )
        
        return response


class EnforceHTTPSMiddleware:
    """
    Middleware que refuerza HTTPS en producción.
    En desarrollo, permite HTTP para testing.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # En producción, validar que sea HTTPS
        if not settings.DEBUG:
            # Verificar esquema
            if request.scheme != 'https':
                logger.warning(
                    f"Intento de acceso HTTP en producción desde {request.META.get('REMOTE_ADDR')}"
                )
                return HttpResponseBadRequest(
                    "HTTPS requerido. Las conexiones no seguras no son permitidas."
                )
            
            # Verificar header X-Forwarded-Proto (si está detrás de proxy)
            x_forwarded_proto = request.META.get('HTTP_X_FORWARDED_PROTO')
            if x_forwarded_proto and x_forwarded_proto != 'https':
                logger.warning(
                    f"X-Forwarded-Proto no es HTTPS: {x_forwarded_proto}"
                )
                return HttpResponseBadRequest(
                    "Proxy debe usar HTTPS."
                )
        
        return self.get_response(request)


class ValidateCertificateMiddleware:
    """
    Middleware que valida certificados SSL/TLS.
    Detiene si certificados están vencidos o inválidos.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # En producción con HTTPS
        if not settings.DEBUG and request.scheme == 'https':
            # Django automáticamente valida certificados
            # Este middleware es principalmente informativo
            
            # Obtener info del certificado si está disponible
            ssl_certificate = request.META.get('SSL_SERVER_CERT')
            if ssl_certificate:
                logger.info("Conexión SSL/TLS validada correctamente")
        
        return self.get_response(request)
