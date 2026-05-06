"""
Gestión Avanzada de Llaves Criptográficas
0.2.3 Key Management
"""

import os
import logging
from datetime import datetime, timedelta
import base64
import json

logger = logging.getLogger(__name__)


# =============================================================================
# 1. ESTRATEGIAS DE ALMACENAMIENTO DE LLAVES
# =============================================================================

class KeyManagementStrategy:
    """
    Estrategias de gestión de llaves en diferentes entornos
    """
    
    # DESARROLLO: Variables de entorno (.env)
    # ✅ Conveniente
    # ⚠️ Vulnerable si .env se expone
    DEVELOPMENT = {
        'method': 'environment_variables',
        'location': '.env file',
        'risk': 'HIGH - Si .env se expone en Git',
        'usage': 'python-dotenv carga automáticamente',
    }
    
    # STAGING: Gestor de Secretos Local
    # ✅ Más seguro que .env
    # ⚠️ Requiere herramienta adicional
    STAGING = {
        'method': 'local_secret_manager',
        'options': [
            'HashiCorp Vault',
            'Kubernetes Secrets',
            'Docker Secrets',
        ],
        'advantage': 'Acceso controlado, auditoría',
    }
    
    # PRODUCCIÓN: Gestor de Secretos Cloud
    # ✅ Estándar de la industria
    # ✅ Rotación automática
    # ✅ Auditoría completa
    PRODUCTION = {
        'method': 'cloud_secret_manager',
        'options': [
            'AWS Secrets Manager',
            'AWS Systems Manager Parameter Store',
            'Google Cloud Secret Manager',
            'Azure Key Vault',
            'HashiCorp Vault',
        ],
    }


class KeyRotationPolicy:
    """
    Política de rotación de llaves
    """
    
    # Intervalo de rotación recomendado
    ROTATION_INTERVAL = timedelta(days=30)  # Cada mes
    
    # Claves a mantener (antigua + nueva)
    KEYS_TO_MAINTAIN = 2
    
    @staticmethod
    def should_rotate(last_rotation_date: datetime) -> bool:
        """
        Determina si la llave debe ser rotada
        """
        days_since_rotation = (datetime.now() - last_rotation_date).days
        return days_since_rotation >= 30
    
    @staticmethod
    def get_rotation_schedule() -> dict:
        """Horario de rotación recomendado"""
        return {
            'frequency': 'Monthly',
            'best_time': 'Low-traffic window (e.g., 2 AM UTC)',
            'backup_before': True,
            'test_after': True,
            'audit_log': True,
        }


# =============================================================================
# 2. GESTIÓN SEGURA DE LLAVES
# =============================================================================

class SecureKeyManager:
    """
    Gestor seguro de llaves criptográficas con auditoría
    """
    
    def __init__(self):
        self.key_access_log = []
    
    def get_key(self, key_id: str = 'PRIMARY') -> bytes:
        """
        Obtiene llave con auditoría
        
        Args:
            key_id: Identificador de la llave (PRIMARY, BACKUP, etc.)
        
        Returns:
            bytes: Clave de 256 bits
        
        Raises:
            KeyError: Si la llave no existe o es inválida
        """
        # ✅ Log de acceso a llave (auditoría)
        self._audit_key_access(key_id, 'GET')
        
        # Obtener llave del gestor de secretos
        try:
            key_b64 = os.environ.get(f"ENCRYPTION_KEY_{key_id}")
            
            if not key_b64:
                logger.error(f"Llave {key_id} no configurada")
                raise KeyError(f"Llave {key_id} no encontrada")
            
            # ✅ Validar formato y tamaño
            key = base64.urlsafe_b64decode(key_b64.encode())
            
            if len(key) != 32:
                logger.error(f"Llave {key_id} tiene tamaño incorrecto")
                raise KeyError(f"Llave {key_id} inválida: tamaño {len(key)} != 32")
            
            logger.info(f"✅ Llave {key_id} obtenida exitosamente")
            return key
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo llave {key_id}: {e}")
            raise
    
    def rotate_key(self, new_key: bytes = None) -> dict:
        """
        Rota la llave criptográfica
        
        Args:
            new_key: Nueva llave (si None, genera una)
        
        Returns:
            dict: Información de rotación
        """
        # ✅ Generar o validar nueva llave
        if new_key is None:
            new_key = os.urandom(32)
        
        if len(new_key) != 32:
            raise ValueError("Nueva llave debe ser 256 bits (32 bytes)")
        
        new_key_b64 = base64.urlsafe_b64encode(new_key).decode()
        
        # ✅ Log de auditoría de rotación
        rotation_info = {
            'timestamp': datetime.now().isoformat(),
            'old_key': self._mask_key(os.environ.get('ENCRYPTION_KEY_PRIMARY')),
            'new_key': self._mask_key(new_key_b64),
            'status': 'pending',
            'action': 'KEY_ROTATION',
        }
        
        logger.warning(f"🔄 ROTACIÓN DE LLAVE: {rotation_info}")
        
        # ✅ Actualizar gestor de secretos (NO directamente en .env)
        # En producción: usar AWS Secrets Manager, Vault, etc.
        
        return rotation_info
    
    def _audit_key_access(self, key_id: str, action: str):
        """Log de acceso a llaves para auditoría"""
        audit_entry = {
            'timestamp': datetime.now().isoformat(),
            'key_id': key_id,
            'action': action,
            'source': 'encryption_module',
        }
        
        self.key_access_log.append(audit_entry)
        
        # ✅ Loguear a archivo de auditoría (no a stdout)
        logger.debug(f"🔐 Auditoría de Llave: {audit_entry}")
    
    @staticmethod
    def _mask_key(key_b64: str) -> str:
        """Enmascara llave para logs (solo últimos 8 caracteres)"""
        if not key_b64:
            return "***MISSING***"
        return f"***{key_b64[-8:]}"
    
    def get_audit_log(self) -> list:
        """Obtiene log de auditoría de acceso a llaves"""
        return self.key_access_log


# =============================================================================
# 3. CONFIGURACIÓN POR ENTORNO
# =============================================================================

class EnvironmentKeyConfig:
    """
    Configuración de gestión de llaves por entorno
    """
    
    # DESARROLLO
    DEVELOPMENT = {
        'storage': 'environment_variables (.env)',
        'validation': True,
        'rotation': False,  # No rotar en desarrollo
        'audit': False,     # Auditoría opcional
        'backup': False,
        'instructions': '''
        1. Generar clave:
           python -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"
        
        2. Agregar a .env:
           ENCRYPTION_KEY=<tu_clave>
        
        3. .gitignore debe incluir:
           *.env
           .env.local
           .env.*.local
        ''',
    }
    
    # STAGING
    STAGING = {
        'storage': 'HashiCorp Vault o Docker Secrets',
        'validation': True,
        'rotation': True,   # Rotar cada 30 días
        'audit': True,
        'backup': True,
        'instructions': '''
        1. Installar Vault:
           curl https://releases.hashicorp.com/vault/... | tar xz
        
        2. Inicializar:
           vault secrets enable -version=2 kv
        
        3. Almacenar llave:
           vault kv put secret/django/encryption_key value=<tu_clave>
        
        4. Recuperar en Django:
           import hvac
           client = hvac.Client(url='http://vault:8200')
           secret = client.secrets.kv.read_secret_version(path='django/encryption_key')
        ''',
    }
    
    # PRODUCCIÓN
    PRODUCTION = {
        'storage': 'AWS Secrets Manager o Azure Key Vault',
        'validation': True,
        'rotation': True,   # Rotar cada 30 días (automático)
        'audit': True,      # Auditoría completa con CloudTrail
        'backup': True,     # Backups encriptados
        'instructions': '''
        1. AWS Secrets Manager:
           aws secretsmanager create-secret --name django/encryption_key --secret-string <tu_clave>
        
        2. Django (boto3):
           import boto3
           client = boto3.client('secretsmanager')
           secret = client.get_secret_value(SecretId='django/encryption_key')
           ENCRYPTION_KEY = secret['SecretString']
        
        3. Rotación automática (cada 30 días):
           aws secretsmanager rotate-secret --secret-id django/encryption_key --rotation-rules {AutomaticallyAfterDays=30}
        
        4. Auditoría (CloudTrail):
           - Todos los accesos se registran automáticamente
           - Configurar alertas para accesos anormales
        ''',
    }


# =============================================================================
# 4. MEJORES PRÁCTICAS
# =============================================================================

BEST_PRACTICES = {
    '1_NUNCA_hardcode': {
        'description': 'Nunca hardcodear llaves en código',
        'bad': '''
        ENCRYPTION_KEY = "uSBOVk0guOL4-ZPZCeMgDOA_m2JuoHggPojwvvjpLAc="  # ❌ MALO
        ''',
        'good': '''
        ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")  # ✅ BIEN
        ''',
    },
    
    '2_Usar_gestor_secretos': {
        'description': 'En producción, usar gestor de secretos profesional',
        'options': [
            'AWS Secrets Manager',
            'Azure Key Vault',
            'Google Cloud Secret Manager',
            'HashiCorp Vault',
        ],
        'benefit': 'Rotación automática, auditoría, control de acceso',
    },
    
    '3_Rotar_llaves': {
        'description': 'Rotar llaves regularmente (cada 30 días)',
        'process': [
            'Generar nueva llave',
            'Desencriptar datos con llave antigua',
            'Reencriptar con llave nueva',
            'Mantener llave antigua para lectura (30 días)',
            'Eliminar llave antigua después del período',
        ],
    },
    
    '4_Auditoría_completa': {
        'description': 'Log de todos los accesos a llaves',
        'log': [
            'Quién accedió',
            'Cuándo',
            'Desde dónde',
            'Acción realizada',
        ],
        'tool': 'CloudTrail (AWS), Activity Log (Azure)',
    },
    
    '5_Backup_seguro': {
        'description': 'Backups de llaves encriptados en lugar seguro',
        'backup_location': [
            'Bóveda física (HSM - Hardware Security Module)',
            'Servicio de escrow de claves',
            'Múltiples regiones geográficas',
        ],
    },
    
    '6_Control_acceso': {
        'description': 'Acceso a llaves solo quién lo necesita',
        'permissions': [
            'Solo aplicación Django',
            'No acceso desde consola',
            'No acceso desde Git',
            'Auditoría si alguien accede',
        ],
    },
    
    '7_Respuesta_incidente': {
        'description': 'Plan si llave se compromete',
        'steps': [
            '1. Inmediatamente revocar llave',
            '2. Generar llave nueva',
            '3. Reencriptar todos los datos',
            '4. Notificar a usuarios/socios',
            '5. Auditoría forense',
        ],
    },
}


# =============================================================================
# 5. EJEMPLO DE IMPLEMENTACIÓN PRODUCCIÓN (AWS)
# =============================================================================

class AWSSecretManagerKeyProvider:
    """
    Proveedor de llaves desde AWS Secrets Manager
    (Ejemplo de producción)
    """
    
    def __init__(self, secret_name: str = 'django/encryption-key'):
        import boto3
        
        self.client = boto3.client('secretsmanager')
        self.secret_name = secret_name
        self.cache = None
        self.cache_expiry = None
    
    def get_key(self, use_cache: bool = True) -> bytes:
        """
        Obtiene llave de AWS Secrets Manager
        
        Args:
            use_cache: Cachear por 5 minutos (reduce latencia)
        """
        # ✅ Cache para reducir llamadas a AWS
        if use_cache and self.cache and datetime.now() < self.cache_expiry:
            logger.info("✅ Llave obtenida de cache")
            return self.cache
        
        try:
            # ✅ Auditoría automática en AWS (CloudTrail)
            response = self.client.get_secret_value(
                SecretId=self.secret_name
            )
            
            key_b64 = response['SecretString']
            key = base64.urlsafe_b64decode(key_b64.encode())
            
            # ✅ Cachear por 5 minutos
            self.cache = key
            self.cache_expiry = datetime.now() + timedelta(minutes=5)
            
            logger.info("✅ Llave obtenida de AWS Secrets Manager")
            return key
            
        except Exception as e:
            logger.error(f"❌ Error obteniendo llave de AWS: {e}")
            raise


# =============================================================================
# 6. CONFIGURACIÓN SEGURA PARA .env (DESARROLLO)
# =============================================================================

SECURE_ENV_SETUP = """
# .env (DESARROLLO SOLO)
# ⚠️ NUNCA COMMITEAR ESTE ARCHIVO

# 1. Generar clave segura:
# python -c "import base64, os; print(base64.urlsafe_b64encode(os.urandom(32)).decode())"

ENCRYPTION_KEY=TU_CLAVE_AQUI

# 2. Configurar .gitignore:
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
echo ".env.*.local" >> .gitignore

# 3. Permisos restrictivos:
chmod 600 .env

# 4. En .env.example (versión pública - SIN VALORES):
# ENCRYPTION_KEY=TU_CLAVE_AQUI
# DB_PASSWORD=tu_contraseña_aqui
"""
