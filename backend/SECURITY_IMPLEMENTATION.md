# Implementación de Seguridad en Reposo - 0.2.1 Cifrado en Reposo

## 📋 Resumen de la Implementación

Se ha implementado un sistema completo de protección de datos en reposo basado en criptografía moderna:

### ✅ Componentes Implementados

#### 1. **Hashing de Contraseñas: Argon2id**
- **Ubicación**: `core/settings.py`
- **Configuración**: Django utiliza automáticamente Argon2id como primer hasher
- **Características**:
  - Incorpora sal (salt) aleatoria automáticamente
  - Resiste ataques de fuerza bruta y rainbow tables
  - Totalmente configurable en Django

```python
# settings.py
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    # ... otros hashers como fallback
]
```

#### 2. **Cifrado de Datos Sensibles: AES-256-GCM**
- **Ubicación**: `utils/aes_gcm.py`
- **Características**:
  - Algoritmo: AES-256 en modo GCM (AEAD - Authenticated Encryption)
  - Nonce aleatorio de 96 bits en cada encriptación
  - Verificación automática de integridad (detecta alteraciones)
  - Soporte completo para Unicode
  
```python
from utils import encrypt_data, decrypt_data

# Encriptar
email_encriptado = encrypt_data("usuario@ejemplo.com")

# Desencriptar
email_original = decrypt_data(email_encriptado)
```

#### 3. **Gestión de Claves de Encriptación**
- **Ubicación**: `utils/aes_gcm.py` (función `_get_encryption_key`)
- **Almacenamiento**: Variable de entorno `ENCRYPTION_KEY` en `.env`
- **Validación**: Verifica que la clave sea exactamente 256 bits (32 bytes)

```python
# .env
ENCRYPTION_KEY=uSBOVk0guOL4-ZPZCeMgDOA_m2JuoHggPojwvvjpLAc=
```

**Para generar una nueva clave**:
```bash
python -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"
```

## 🔐 Características de Seguridad

### AES-256-GCM
- **Confidencialidad**: Los datos no se pueden leer sin la clave
- **Integridad**: Se detectan automáticamente datos alterados
- **Autenticidad**: Se valida la procedencia de los datos
- **Nonce Aleatorio**: Cada encriptación produce output diferente (no determinista)

### Manejo de Errores
```python
from utils import encrypt_data, decrypt_data, InvalidCiphertextError

try:
    datos = decrypt_data(ciphertext)
except InvalidCiphertextError as e:
    # Los datos fueron alterados o la clave es incorrecta
    print(f"Error de integridad: {e}")
```

## 📁 Estructura de Archivos

```
backend/
├── utils/
│   ├── __init__.py              # Exporta funciones de encriptación
│   ├── aes_gcm.py              # Implementación AES-256-GCM
│   └── ejemplo_encriptacion.py  # Ejemplos de uso
├── core/
│   └── settings.py              # Configuración Argon2id (modificado)
├── .env                         # ENCRYPTION_KEY (modificado)
├── requirements.txt             # cryptography, argon2-cffi (modificado)
├── demo_encryption.py           # Demostración funcional
└── test_encryption.py           # Suite de pruebas
```

## 🚀 Uso en el Proyecto

### Opción 1: En Modelos Django

```python
from django.db import models
from utils import encrypt_data, decrypt_data

class Persona(models.Model):
    nombre = models.CharField(max_length=255)
    _email_encrypted = models.TextField(null=True)
    
    @property
    def email(self):
        if self._email_encrypted:
            return decrypt_data(self._email_encrypted)
        return None
    
    @email.setter
    def email(self, value):
        if value:
            self._email_encrypted = encrypt_data(value)
```

### Opción 2: En Vistas/Servicios

```python
from utils import encrypt_data, decrypt_data

def crear_usuario(request):
    email = request.POST['email']
    email_encriptado = encrypt_data(email)
    
    # Guardar en BD
    usuario = Usuario.objects.create(
        email_encrypted=email_encriptado
    )
```

### Opción 3: En Serializers DRF

```python
from rest_framework import serializers
from utils import encrypt_data, decrypt_data

class PersonaSerializer(serializers.Serializer):
    nombre = serializers.CharField()
    email = serializers.EmailField()
    
    def create(self, validated_data):
        validated_data['email'] = encrypt_data(validated_data['email'])
        return Persona.objects.create(**validated_data)
```

## 🧪 Pruebas

### Ejecutar Demostración
```bash
cd backend
python demo_encryption.py
```

### Resultado Esperado
```
============================================================
DEMOSTRACIÓN: AES-256-GCM para Protección en Reposo
============================================================

[1] ENCRIPTACIÓN Y DESENCRIPTACIÓN BÁSICA
✅ Verificación: EXITOSA

[2] NONCE ALEATORIO (CADA ENCRIPTACIÓN ES DIFERENTE)
✅ Verificación: EXITOSA

[3] VERIFICACIÓN DE INTEGRIDAD (DETECTAR ALTERACIONES)
✅ Integridad comprometida detectada

[4] SOPORTE PARA UNICODE Y CARACTERES ESPECIALES
✅ Verificación: EXITOSA

[5] INFORMACIÓN TÉCNICA
✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE
```

## 📦 Dependencias Instaladas

```
cryptography==42.0.5      # Implementación de AES-256-GCM
argon2-cffi==25.1.0       # Implementación de Argon2id
python-dotenv==1.0.0      # Carga de variables de entorno
```

## ⚙️ Configuración en Django

El archivo `core/settings.py` ha sido actualizado para:

1. **Cargar variables de entorno** desde `.env`
```python
from dotenv import load_dotenv
load_dotenv(dotenv_path)
```

2. **Configurar Argon2id como primer hasher**
```python
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    # ...
]
```

## 🔍 Validaciones Implementadas

### En Encriptación
- ✅ Verifica que el plaintext sea string
- ✅ Obtiene clave validada desde variables de entorno
- ✅ Genera nonce aleatorio de 96 bits
- ✅ Proporciona confidencialidad e integridad

### En Desencriptación
- ✅ Valida que ciphertext sea string
- ✅ Valida longitud mínima del ciphertext
- ✅ Detecta automáticamente datos alterados (InvalidTag)
- ✅ Valida base64 válido
- ✅ Proporciona mensajes de error informativos

## 🛡️ Recomendaciones de Seguridad

### Para Producción

1. **Clave de Encriptación**
   - Cambiar `ENCRYPTION_KEY` por una nueva antes de deploy
   - Guardar en gestor de secretos (AWS Secrets Manager, HashiCorp Vault, etc.)
   - NUNCA commitear en Git

2. **Rotación de Claves**
   - Implementar estrategia de rotación periódica
   - Mantener claves antiguas para desencriptación de datos históricos
   - Reencriptar datos con clave nueva

3. **Base de Datos**
   - Usar cifrado a nivel de BD (TDE, Transparent Data Encryption)
   - Backups encriptados
   - Conexiones SSL/TLS a base de datos

4. **Logs**
   - NUNCA loguear datos sensibles encriptados
   - Loguear solo hashes o IDs
   - Revisar logs regularmente

5. **Auditoría**
   - Registrar quién accede a datos sensibles
   - Monitoreo de intentos de desencriptación fallidos
   - Alertas en caso de anomalías

## 📚 Referencias

- [OWASP: Storing Passwords](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [NIST: Guidelines on Cryptographic Algorithms](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-175B.pdf)
- [Django: Password Management](https://docs.djangoproject.com/en/6.0/topics/auth/passwords/)
- [Cryptography.io Documentation](https://cryptography.io/en/latest/)
- [Argon2 White Paper](https://github.com/P-H-C/phc-winner-argon2/blob/master/argon2-specs.pdf)

## ❓ Preguntas Frecuentes

### ¿Qué pasa si pierdo la ENCRYPTION_KEY?
Los datos encriptados serán irrecuperables. Asegúrate de:
- Hacer backup de la clave en lugar seguro
- Usar gestor de secretos
- Tener procedimiento de recuperación de desastres

### ¿Puedo cambiar la clave?
Sí, pero necesitas reencriptar todos los datos:
1. Obtener todos los datos con clave antigua
2. Desencriptar con clave antigua
3. Encriptar con clave nueva
4. Guardar en BD

### ¿Overhead de rendimiento?
Mínimo (~1-5ms por operación):
- AES-256-GCM es hardware-acelerado en CPUs modernas
- Solo aplica a datos específicamente marcados como sensibles
- BD caching alivia la mayoría de operaciones

### ¿Compatible con migraciones de BD?
Sí:
- Campos encriptados se guardan como TextField
- Se pueden crear sin problemas
- Los datos ya encriptados se preservan

## ✨ Mejoras Futuras

1. **Cifrado a nivel de BD** (PostgeSQL native encryption)
2. **Key Derivation Function (KDF)** para contraseñas basadas en clave maestra
3. **Field-level Encryption middleware**
4. **Automatic key rotation**
5. **Hardware security module (HSM) integration**

---

**Estado**: ✅ Implementado y Probado
**Versión**: 0.2.1 - Cifrado en Reposo
**Última Actualización**: 2026-04-30
