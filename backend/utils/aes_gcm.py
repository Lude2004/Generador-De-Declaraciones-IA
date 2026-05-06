"""
Módulo de encriptación AES-256-GCM para protección de datos en reposo.
Proporciona confidencialidad e integridad mediante AEAD cipher.
"""

import os
import base64
import logging
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

logger = logging.getLogger(__name__)


class EncryptionError(Exception):
    """Excepción base para errores de encriptación."""
    pass


class InvalidCiphertextError(EncryptionError):
    """Se lanza cuando el texto cifrado es inválido o ha sido alterado."""
    pass


class EncryptionKeyError(EncryptionError):
    """Se lanza cuando hay problemas con la clave de encriptación."""
    pass


def _get_encryption_key() -> bytes:
    """
    Obtiene y valida la clave de encriptación desde variables de entorno.
    
    Returns:
        bytes: Clave de encriptación de 256 bits (32 bytes).
        
    Raises:
        EncryptionKeyError: Si la clave no existe o es inválida.
    """
    key_b64 = os.environ.get("ENCRYPTION_KEY")
    
    if not key_b64:
        raise EncryptionKeyError(
            "Variable de entorno ENCRYPTION_KEY no configurada. "
            "Genérala con: python -c \"import base64, os; "
            "print(base64.urlsafe_b64encode(os.urandom(32)).decode())\""
        )
    
    try:
        key = base64.urlsafe_b64decode(key_b64.encode())
        
        if len(key) != 32:
            raise EncryptionKeyError(
                f"Clave de encriptación inválida: debe ser 256 bits (32 bytes), "
                f"se recibió {len(key) * 8} bits"
            )
        
        return key
    except Exception as e:
        raise EncryptionKeyError(f"No se pudo decodificar ENCRYPTION_KEY: {str(e)}")


def encrypt_data(plaintext: str) -> str:
    """
    Encripta datos usando AES-256-GCM.
    
    Args:
        plaintext (str): Texto plano a encriptar.
        
    Returns:
        str: Texto cifrado en formato base64 (nonce + ciphertext).
        
    Raises:
        EncryptionError: Si ocurre un error durante la encriptación.
    """
    if not isinstance(plaintext, str):
        raise EncryptionError("El texto plano debe ser una cadena (str)")
    
    try:
        key = _get_encryption_key()
        
        # Generar nonce aleatorio de 96 bits (12 bytes)
        # Unicidad del nonce es crítica para AES-GCM
        nonce = os.urandom(12)
        
        # Crear cifrador AESGCM
        cipher = AESGCM(key)
        
        # Encriptar: proporciona confidencialidad e integridad
        ciphertext = cipher.encrypt(nonce, plaintext.encode('utf-8'), None)
        
        # Combinar nonce + ciphertext y codificar en base64
        # El nonce es público y no necesita ocultarse
        encrypted_data = base64.b64encode(nonce + ciphertext).decode('utf-8')
        
        return encrypted_data
        
    except EncryptionKeyError:
        raise
    except Exception as e:
        logger.error(f"Error durante encriptación: {type(e).__name__}")
        raise EncryptionError(f"Fallo al encriptar datos: {type(e).__name__}")


def decrypt_data(ciphertext: str) -> str:
    """
    Desencripta datos usando AES-256-GCM.
    
    Args:
        ciphertext (str): Texto cifrado en formato base64.
        
    Returns:
        str: Texto plano desencriptado.
        
    Raises:
        InvalidCiphertextError: Si el texto cifrado es inválido o ha sido alterado.
        EncryptionError: Si ocurre otro error durante la desencriptación.
    """
    if not isinstance(ciphertext, str):
        raise InvalidCiphertextError("El texto cifrado debe ser una cadena (str)")
    
    try:
        key = _get_encryption_key()
        
        # Decodificar desde base64
        data = base64.b64decode(ciphertext.encode('utf-8'))
        
        # Validar longitud mínima (12 bytes de nonce + al menos 16 bytes de tag)
        if len(data) < 28:
            raise InvalidCiphertextError("Texto cifrado corrupto: longitud insuficiente")
        
        # Separar nonce y ciphertext
        nonce = data[:12]
        encrypted_ciphertext = data[12:]
        
        # Crear cifrador AESGCM
        cipher = AESGCM(key)
        
        # Desencriptar y verificar integridad (el tag se valida automáticamente)
        plaintext = cipher.decrypt(nonce, encrypted_ciphertext, None)
        
        return plaintext.decode('utf-8')
        
    except EncryptionKeyError:
        raise
    except InvalidCiphertextError:
        raise
    except Exception as e:
        # InvalidTag se lanza si la integridad fue comprometida
        if "InvalidTag" in str(type(e)):
            logger.warning("Intento de desencriptación fallido: datos alterados o clave incorrecta")
            raise InvalidCiphertextError("Fallo en verificación de integridad: datos pueden estar alterados")
        
        logger.error(f"Error durante desencriptación: {type(e).__name__}")
        raise EncryptionError(f"Fallo al desencriptar datos: {type(e).__name__}")


# Funciones de utilidad para campos de modelo Django

class EncryptedField:
    """
    Descriptor para campos encriptados en modelos Django.
    Uso: En models.py después de un CharField
    """
    def __init__(self, field_name):
        self.field_name = field_name
        self.encrypted_field = f"_{field_name}_encrypted"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        encrypted_value = getattr(obj, self.encrypted_field, None)
        if encrypted_value:
            try:
                return decrypt_data(encrypted_value)
            except Exception as e:
                logger.error(f"Error desencriptando {self.field_name}: {e}")
                return None
        return None
    
    def __set__(self, obj, value):
        if value is not None:
            try:
                encrypted_value = encrypt_data(str(value))
                setattr(obj, self.encrypted_field, encrypted_value)
            except Exception as e:
                logger.error(f"Error encriptando {self.field_name}: {e}")
        else:
            setattr(obj, self.encrypted_field, None)
