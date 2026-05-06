# Gestión de Llaves Criptográficas
## 0.2.3 Key Management - Comparativa y Análisis

---

## 📊 **TU PROPUESTA vs LO IMPLEMENTADO**

### 🔴 **Tu Propuesta (Básica)**

```python
import os
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")

# En bash:
export ENCRYPTION_KEY="TU_CLAVE_SEGURA"
```

**Características:**
- ✅ Variables de entorno (correcto)
- ✅ No hardcoding (correcto)
- ✅ Separación física/lógica (correcto)
- ⚠️ Sin validación
- ⚠️ Sin manejo de errores
- ⚠️ Sin auditoría
- ⚠️ Sin rotación

**Riesgo:** ⚠️ **ALTO** - Si la llave falta o es inválida, silenciosamente falla

---

### 🟢 **Lo Implementado (Profesional)**

**Archivo:** [utils/aes_gcm.py](utils/aes_gcm.py)

```python
def _get_encryption_key() -> bytes:
    # ✅ 1. Obtiene de variables de entorno (como tú)
    key_b64 = os.environ.get("ENCRYPTION_KEY")
    
    # ✅ 2. VALIDA existencia
    if not key_b64:
        raise EncryptionKeyError(
            "Variable ENCRYPTION_KEY no configurada. "
            "Genérala con: python -c '...'"
        )
    
    # ✅ 3. VALIDA decodificación base64
    key = base64.urlsafe_b64decode(key_b64.encode())
    
    # ✅ 4. VALIDA tamaño (256 bits = 32 bytes)
    if len(key) != 32:
        raise EncryptionKeyError(
            f"Clave inválida: {len(key)*8} bits, se requieren 256"
        )
    
    return key
```

**Mejoras:**
- ✅ Validación de existencia
- ✅ Validación de formato (base64)
- ✅ Validación de tamaño
- ✅ Mensajes de error claros
- ✅ Excepción personalizada

---

## 🔐 **MATRIZ DE GESTIÓN DE LLAVES**

| Característica | Tu Propuesta | Implementado | Producción |
|----------------|-------------|--------------|-----------|
| **Variables Entorno** | ✅ | ✅ | ✅ |
| **Validación** | ❌ | ✅ | ✅ |
| **Auditoría** | ❌ | ❌ | ✅ CRÍTICO |
| **Rotación** | ❌ | ❌ | ✅ CRÍTICO |
| **Backup Seguro** | ❌ | ❌ | ✅ CRÍTICO |
| **Control Acceso** | ❌ | ❌ | ✅ CRÍTICO |
| **Gestor Secretos** | ❌ | ❌ | ✅ (AWS/Vault) |
| **Plan de Incidente** | ❌ | ❌ | ✅ CRÍTICO |

---

## 🎯 **COMPARATIVA POR ENTORNO**

### 1️⃣ DESARROLLO

#### Tu Enfoque
```bash
export ENCRYPTION_KEY="TU_CLAVE"
# ⚠️ Problemático: Queda en bash history
```

#### Lo Implementado
```bash
# .env (ignorado en Git)
ENCRYPTION_KEY=uSBOVk0guOL4-ZPZCeMgDOA_m2JuoHggPojwvvjpLAc=

# python-dotenv carga automáticamente
from dotenv import load_dotenv
load_dotenv()
```

**Mejora:** 🟢 `.env` es más seguro que `export` (no queda en history)

---

### 2️⃣ STAGING

#### Tu Enfoque
```
(No especificado)
```

#### Recomendado
```bash
# Opción 1: Vault local
vault secrets enable -version=2 kv
vault kv put secret/django/encryption_key value=...

# Opción 2: Docker Secrets
echo "TU_CLAVE" | docker secret create django_encryption_key -

# Opción 3: Kubernetes Secrets
kubectl create secret generic django-encryption-key --from-literal=key=...
```

**Beneficio:** Gestión centralizada, auditoría, rotación automática

---

### 3️⃣ PRODUCCIÓN

#### Tu Enfoque
```
(No especificado)
```

#### CORRECTO - AWS Secrets Manager
```python
import boto3
import json

client = boto3.client('secretsmanager', region_name='us-east-1')

# Obtener llave
response = client.get_secret_value(SecretId='django/encryption-key')
ENCRYPTION_KEY = response['SecretString']

# Rotación automática cada 30 días
client.rotate_secret(
    SecretId='django/encryption-key',
    RotationRules={'AutomaticallyAfterDays': 30}
)
```

**Beneficios:**
- ✅ Rotación automática
- ✅ Auditoría automática (CloudTrail)
- ✅ Control de acceso granular
- ✅ Cumplimiento normativo (PCI-DSS, HIPAA)

---

## ⚠️ **RIESGOS: Tu Propuesta vs Producción**

### ❌ RIESGOS TU PROPUESTA

| Riesgo | Impacto | Mitigación |
|--------|---------|-----------|
| **Llave en bash history** | 🔴 CRÍTICO | Usar .env en lugar de export |
| **Sin validación** | 🔴 CRÍTICO | Validar en _get_encryption_key() |
| **Sin rotación** | 🔴 CRÍTICO | Implementar rotación cada 30 días |
| **Sin auditoría** | 🔴 CRÍTICO | CloudTrail, logs estructurados |
| **Sin backup** | 🔴 CRÍTICO | Backup en HSM, múltiples regiones |
| **Si .env se filtra en Git** | 🔴 CRÍTICO | Agregar a .gitignore, verificar history |
| **Acceso sin control** | 🟡 ALTO | Permisos restrictivos en .env |

---

## ✅ **LO QUE YA ESTÁ BIEN IMPLEMENTADO**

### 1. Validación de Clave
✅ [utils/aes_gcm.py](utils/aes_gcm.py) - Líneas 40-60

```python
# Valida que sea 256 bits exactamente
if len(key) != 32:
    raise EncryptionKeyError(
        f"Clave debe ser 256 bits, se recibió {len(key)*8} bits"
    )
```

### 2. Manejo de Errores
✅ [utils/aes_gcm.py](utils/aes_gcm.py) - EncryptionKeyError

```python
class EncryptionKeyError(EncryptionError):
    """Se lanza cuando hay problemas con la clave"""
    pass
```

### 3. Carga Automática desde .env
✅ [core/settings.py](core/settings.py) - Líneas 16-18

```python
from dotenv import load_dotenv
load_dotenv(dotenv_path)
```

### 4. .gitignore Protegido
✅ [.gitignore](.gitignore)

```
.env
.env.local
.env.*.local
*.key
```

---

## 🚀 **QUÉ FALTA PARA PRODUCCIÓN**

### 1️⃣ **ROTACIÓN DE LLAVES** 🔄
```python
# TODO: Implementar
def rotate_encryption_key():
    """Rota llave cada 30 días"""
    
    new_key = os.urandom(32)  # Generar nueva
    old_key = _get_encryption_key()  # Guardar vieja
    
    # Reencriptar datos
    for data in get_all_encrypted_data():
        plaintext = decrypt_data(data, old_key)
        encrypted = encrypt_data(plaintext, new_key)
        save(encrypted)
    
    # Actualizar en gestor de secretos
    # (NO en .env)
```

### 2️⃣ **AUDITORÍA DE ACCESO A LLAVES** 📝
```python
# TODO: Implementar
class KeyAuditLogger:
    def log_access(self, action: str, key_id: str, user: str):
        """Log de acceso a llaves"""
        audit_entry = {
            'timestamp': datetime.now(),
            'action': action,
            'key_id': key_id,
            'user': user,
            'result': 'success',
        }
        
        # Guardar en base de datos separada (no lossy logs)
        save_to_audit_log(audit_entry)
```

### 3️⃣ **GESTOR DE SECRETOS CLOUD** ☁️
```python
# TODO: AWS Secrets Manager
import boto3

client = boto3.client('secretsmanager')

# En producción:
response = client.get_secret_value(
    SecretId='django/encryption-key'
)
ENCRYPTION_KEY = response['SecretString']

# Rotación automática
client.rotate_secret(
    SecretId='django/encryption-key',
    RotationRules={'AutomaticallyAfterDays': 30}
)
```

### 4️⃣ **BACKUP SEGURO DE LLAVES** 💾
```
Ubicaciones recomendadas:
1. AWS Secrets Manager (primario)
2. AWS Backup (redundancia)
3. HSM (Hardware Security Module)
4. Escrow de claves externo (recuperación de desastres)

NUNCA: GitHub, Email, Dropbox, USB sin encriptación
```

### 5️⃣ **CONTROL DE ACCESO** 🔐
```bash
# .env debe tener permisos restrictivos
chmod 600 .env

# Solo para lectura (no ejecución)
# No exponer a navegador/client
```

### 6️⃣ **PLAN DE INCIDENTE** 🚨
```
Si llave se compromete:
1. ⚠️ INMEDIATAMENTE: Revocar llave comprometida
2. ⚠️ INMEDIATAMENTE: Generar llave nueva
3. [1 hora] Reencriptar datos sensibles
4. [1 día] Notificar a usuarios/socios
5. [1 semana] Auditoría forense
6. [2 semanas] Postmortem y mejoras
```

---

## 📋 **CHECKLIST: GESTIÓN DE LLAVES**

### Desarrollo ✅
- [x] Variables de entorno (.env)
- [x] Validación de clave
- [x] Manejo de errores
- [x] .gitignore configurado
- [ ] Rotación manual documentada

### Staging ⚠️
- [ ] Gestor de secretos (Vault/K8s)
- [ ] Auditoría de acceso
- [ ] Backup de llaves
- [ ] Plan de rotación
- [ ] Plan de incidente

### Producción ❌
- [ ] AWS Secrets Manager
- [ ] CloudTrail para auditoría
- [ ] Rotación automática cada 30 días
- [ ] Backup en múltiples regiones
- [ ] Plan de incidente y recuperación
- [ ] HSM para claves críticas
- [ ] Cumplimiento normativo (PCI-DSS, HIPAA, etc.)

---

## 🎓 **CONCLUSIÓN**

### Tu Propuesta
✅ **Correcto en concepto pero INCOMPLETO**
- Idea fundamental sólida
- Pero le faltan validaciones y seguridad
- No es suficiente para producción

### Lo Implementado
✅ **Sólido para desarrollo/staging**
- Validaciones correctas
- Manejo de errores
- Documentado
- **Aún necesita**: Rotación, auditoría, gestor de secretos para producción

### Recomendación Final
1. **Ahora** (Desarrollo): ✅ Está bien
2. **Antes de Staging**: Agregar rotación y auditoría
3. **Antes de Producción**: AWS Secrets Manager + CloudTrail

---

**Archivo de Referencia Completo:** [utils/key_management.py](utils/key_management.py)
