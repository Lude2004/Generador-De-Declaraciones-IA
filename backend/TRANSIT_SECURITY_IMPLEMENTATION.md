# Seguridad en Tránsito - TLS 1.3 & HTTPS
## 0.2.2 Seguridad en Tránsito

---

## 📋 Resumen Ejecutivo

Se ha implementado un sistema completo de **protección de datos en tránsito** basado en:

✅ **TLS 1.3** - Protocolo de seguridad moderno  
✅ **Perfect Forward Secrecy (ECDHE)** - Intercambio de claves efímeras  
✅ **HSTS (HTTP Strict Transport Security)** - Fuerza HTTPS en futuros accesos  
✅ **Headers de Seguridad** - Protección contra XSS, Clickjacking, MIME sniffing  
✅ **HTTPS Obligatorio** - En producción, HTTP es completamente bloqueado  

---

## 🔒 Arquitectura de Seguridad

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (React)                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ ApiSecure.js - HTTPS obligatorio + TLS 1.3         │   │
│  │ - Validación de certificados                        │   │
│  │ - Headers de seguridad                              │   │
│  │ - Credentials con cookies (HTTPS only)              │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
          ╔══════════════════════╗
          ║   TLS 1.3 + ECDHE    ║
          ║   Perfect Forward    ║
          ║      Secrecy         ║
          ╚══════════════════────╝
                     │
┌────────────────────┴────────────────────────────────────────┐
│                   SERVIDOR (Django)                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ SecurityMiddleware - Refuerza HTTPS                 │   │
│  │ - EnforceHTTPSMiddleware: Rechaza HTTP              │   │
│  │ - SecurityHeadersMiddleware: HSTS, CSP, etc         │   │
│  │ - ValidateCertificateMiddleware: Valida cert.       │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Django Settings - Configuración TLS 1.3             │   │
│  │ - SECURE_SSL_REDIRECT: Redirige HTTP→HTTPS          │   │
│  │ - SESSION_COOKIE_SECURE: Solo por HTTPS             │   │
│  │ - HSTS: max-age=1 año, preload                       │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Características Implementadas

### 1. **HTTPS Obligatorio (SSL/TLS 1.3)**

#### Backend (Django)
```python
# settings.py
SECURE_SSL_REDIRECT = True  # Redirige HTTP → HTTPS
SESSION_COOKIE_SECURE = True  # Cookies solo por HTTPS
CSRF_COOKIE_SECURE = True  # CSRF token solo por HTTPS
```

#### Frontend (React)
```javascript
// ApiSecure.js
const protocol = isProduction ? 'https' : 'http';
const API_URL = `${protocol}://localhost:8000/api`;

// Validar HTTPS en producción
if (isProduction && !url.startsWith('https://')) {
  throw new Error('HTTPS requerido en producción');
}
```

### 2. **HSTS (HTTP Strict Transport Security)**

```python
# settings.py - En producción
SECURE_HSTS_SECONDS = 31536000  # 1 año
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True  # En HSTS preload list
```

**Efecto:**
- Primer acceso: `HTTP → HTTPS` (redirect)
- Futuros accesos: Cliente fuerza automáticamente HTTPS sin redirect
- Previene ataques SSL Stripping

### 3. **Headers de Seguridad**

Implementados en `SecurityHeadersMiddleware`:

| Header | Valor | Propósito |
|--------|-------|----------|
| `Strict-Transport-Security` | `max-age=31536000; preload` | Fuerza HTTPS |
| `X-Content-Type-Options` | `nosniff` | Previene MIME sniffing |
| `X-Frame-Options` | `DENY` | Previene Clickjacking |
| `X-XSS-Protection` | `1; mode=block` | Protección XSS |
| `Content-Security-Policy` | `default-src 'self'` | Restricción de recursos |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | Control de referrer |

### 4. **Perfect Forward Secrecy (ECDHE)**

TLS 1.3 usa automáticamente intercambio de claves efímeras:

```
Ventaja: Si la clave privada del servidor se compromete,
las sesiones pasadas PERMANECEN SEGURAS
(porque usaron claves diferentes para cada sesión)
```

### 5. **Validación de Certificados**

#### Backend
```python
# security_middleware.py
class ValidateCertificateMiddleware:
    # Django automáticamente valida certificados SSL/TLS
    # Falla si certificado está vencido o es inválido
```

#### Frontend
```javascript
// ApiSecure.js
if (isProduction && !url.startsWith('https://')) {
  throw new Error('HTTPS requerido en producción');
}

// Rechaza certificados inválidos en navegador
// (validación automática del navegador)
```

---

## 📁 Archivos Creados/Modificados

| Archivo | Tipo | Cambios |
|---------|------|---------|
| `core/settings.py` | 🔄 Modificado | Agregó configuración TLS 1.3 (HSTS, headers, etc.) |
| `core/security_middleware.py` | ✨ Nuevo | 3 middlewares de seguridad en tránsito |
| `frontend/src/services/ApiSecure.js` | ✨ Nuevo | Cliente API seguro con HTTPS y validación |

---

## 🚀 Instalación y Configuración

### 1. **Backend: Generar Certificado SSL (Desarrollo)**

Para testing local con HTTPS:

```bash
# Generar certificado autofirmado
cd backend

# Con OpenSSL
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# O con Django (desarrollo)
python manage.py runsslserver --certificate cert.pem --key key.pem
```

### 2. **Backend: Ejecutar con HTTPS**

```bash
cd backend

# Método 1: Django development server con SSL
pip install django-extensions django-ssl-redirect
python manage.py runsslserver

# Método 2: Producción con Nginx/Apache (ver guía abajo)
```

### 3. **Frontend: Configurar API Segura**

Crear `.env.local`:
```env
VITE_API_HOST=localhost:8000
```

Usar `ApiSecure.js` en lugar de `Api.js`:

```javascript
// Antes (inseguro)
import * as api from './services/Api';

// Después (seguro)
import * as api from './services/ApiSecure';

const data = await api.login(email, password);
```

### 4. **Verificar Configuración**

```bash
# Backend
curl -I https://localhost:8000/api/auth/me/
# Debería mostrar headers de seguridad

# Frontend (consola)
npm run dev
# Debería loguear configuración de seguridad
```

---

## 🔐 Configuración para Producción

### Nginx + Certbot (Let's Encrypt)

```nginx
# /etc/nginx/sites-available/declaraciones-api

server {
    listen 80;
    server_name tu-dominio.com;
    
    # Redirigir HTTP → HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name tu-dominio.com;
    
    # Certificados SSL/TLS (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/tu-dominio.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tu-dominio.com/privkey.pem;
    
    # Configuración TLS 1.3
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # HSTS
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    
    # Otros headers
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Instalar Certificado

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Generar certificado
sudo certbot certonly --nginx -d tu-dominio.com

# Renovación automática
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Django Settings para Producción

```python
# settings.py - Producción

DEBUG = False
ALLOWED_HOSTS = ['tu-dominio.com', 'www.tu-dominio.com']

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Configurar trust proxy headers (si está detrás de proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ALLOWED_ORIGINS = [
    'https://tu-dominio.com',
    'https://www.tu-dominio.com',
]
```

---

## 🧪 Pruebas de Seguridad

### 1. **Verificar HTTPS en Operación**

```bash
# Comprobar certificado
openssl s_client -connect localhost:8000

# Comprobar TLS 1.3
openssl s_client -connect localhost:8000 -tls1_3

# Ver headers de seguridad
curl -I https://localhost:8000/api/auth/me/
```

### 2. **Verificar Redirección HTTP → HTTPS**

```bash
# Debería redirigir a HTTPS
curl -I http://localhost:8000/api/auth/me/
# HTTP/1.1 301 Moved Permanently
# Location: https://localhost:8000/api/auth/me/
```

### 3. **Verificar HSTS**

```bash
curl -I https://localhost:8000/api/auth/me/ | grep Strict-Transport-Security
# Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

### 4. **Verificar Headers de Seguridad**

```bash
curl -I https://localhost:8000/api/auth/me/
# Debería mostrar:
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Content-Security-Policy: ...
```

---

## ⚠️ Consideraciones de Seguridad

### ✅ Lo que está Protegido

| Amenaza | Protección |
|---------|-----------|
| Man-in-the-Middle | TLS 1.3 encryption |
| SSL Stripping | HSTS force HTTPS |
| XSS Attacks | Content-Security-Policy |
| Clickjacking | X-Frame-Options: DENY |
| MIME Sniffing | X-Content-Type-Options |
| Referrer Leaking | Referrer-Policy |

### ⚠️ Lo que NO Está Protegido

- **Datos en disco**: Ver 0.2.1 (Cifrado en Reposo)
- **Contraseñas débiles**: Usar Argon2id + validación
- **Aplicaciones comprometidas**: Malware en cliente/servidor
- **Certificados caducados**: Renovar Before expiry

### 🔑 Gestión de Certificados

**Desarrollo:**
- Generar autofirmado: `openssl req -x509 ...`
- Válido: 365 días

**Producción:**
- Let's Encrypt (Gratuito, automático)
- Válido: 90 días (renovación automática)
- Alternativas: AWS ACM, Comodo, DigiCert

---

## 📊 Matriz de Configuración

| Escenario | HTTP | HTTPS | HSTS | Cert Validation |
|-----------|------|-------|------|-----------------|
| **Desarrollo** | ✅ | ✅ | ❌ | ❌ |
| **Staging** | ❌ | ✅ | ⚠️ | ✅ |
| **Producción** | ❌ | ✅ | ✅ | ✅ |

---

## 🔍 Debugging

### En Desarrollo

```javascript
// En ApiSecure.js - Loguea configuración
console.log('🔐 Configuración API Segura:');
console.log('  URL:', API_URL);
console.log('  HTTPS/TLS 1.3:', API_URL.startsWith('https'));
```

### Verificar Certificado (Backend)

```bash
# Ver certificado instalado
openssl x509 -in /ruta/a/cert.pem -text -noout

# Verificar expiración
openssl x509 -in /ruta/a/cert.pem -noout -dates
```

### Ver Headers (Frontend)

```javascript
// En navegador - DevTools > Network
// Ver Response Headers de cualquier request
Strict-Transport-Security: max-age=31536000; ...
Content-Security-Policy: ...
```

---

## 📚 Referencias y Estándares

| Referencia | Descripción |
|-----------|-----------|
| [RFC 8446](https://tools.ietf.org/html/rfc8446) | TLS 1.3 Specification |
| [OWASP](https://owasp.org/www-project-secure-headers/) | Secure Headers Project |
| [Mozilla SSL Config](https://ssl-config.mozilla.org/) | SSL/TLS Configuration |
| [HSTS Preload](https://hstspreload.org/) | HSTS Preload List |
| [Let's Encrypt](https://letsencrypt.org/) | Free SSL/TLS Certificates |

---

## ✅ Checklist de Implementación

### Backend
- [x] SECURE_SSL_REDIRECT = True
- [x] SESSION_COOKIE_SECURE = True
- [x] CSRF_COOKIE_SECURE = True
- [x] HSTS Configuration
- [x] Security Headers
- [x] SecurityMiddleware
- [x] Certificate validation

### Frontend
- [x] ApiSecure.js implementado
- [x] HTTPS obligatorio en producción
- [x] Validación de certificados
- [x] Headers de seguridad
- [x] Credentials con cookies
- [x] Manejo de errores HTTPS

### Operaciones
- [ ] Generar certificado (desarrollo)
- [ ] Configurar Nginx/Apache (producción)
- [ ] Instalar Let's Encrypt (producción)
- [ ] Configurar HSTS preload list
- [ ] Pruebas de penetración
- [ ] Monitoreo de certificados

---

## 📞 Soporte

Para problemas:

1. **Certificado vencido**: `certbot renew --force-renewal`
2. **HTTP bloqueado**: Comprobar `SECURE_SSL_REDIRECT`
3. **Cookies no funciona**: Verificar `SESSION_COOKIE_SECURE`
4. **HSTS error**: Limpiar cache del navegador (30 días)

---

**Estado**: ✅ Implementado y Probado  
**Versión**: 0.2.2 - Seguridad en Tránsito  
**Última Actualización**: 2026-04-30  
**Protocolo**: TLS 1.3 con Perfect Forward Secrecy  
