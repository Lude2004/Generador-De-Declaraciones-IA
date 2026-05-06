"""
Ejemplo de uso de encriptación AES-256-GCM en modelos Django.
Este archivo demuestra cómo integrar la seguridad en reposo en tus modelos.
"""

from django.db import models
from utils import encrypt_data, decrypt_data, EncryptionError


# Ejemplo 1: Campo encriptado personalizado
class PersonaEncriptada(models.Model):
    """
    Ejemplo de modelo con campos encriptados.
    Debes crear esto solo como referencia, no ejecutar migraciones sin revisar.
    """
    nombre = models.CharField(max_length=255)
    _email_encrypted = models.TextField(blank=True, null=True, db_column='email')
    _numero_identificacion_encrypted = models.TextField(blank=True, null=True, db_column='numero_identificacion')
    
    class Meta:
        app_label = 'core'
    
    @property
    def email(self):
        """Desencriptar email"""
        if self._email_encrypted:
            try:
                return decrypt_data(self._email_encrypted)
            except EncryptionError as e:
                print(f"Error desencriptando email: {e}")
                return None
        return None
    
    @email.setter
    def email(self, value):
        """Encriptar email"""
        if value:
            try:
                self._email_encrypted = encrypt_data(value)
            except EncryptionError as e:
                print(f"Error encriptando email: {e}")
        else:
            self._email_encrypted = None
    
    @property
    def numero_identificacion(self):
        """Desencriptar número de identificación"""
        if self._numero_identificacion_encrypted:
            try:
                return decrypt_data(self._numero_identificacion_encrypted)
            except EncryptionError as e:
                print(f"Error desencriptando ID: {e}")
                return None
        return None
    
    @numero_identificacion.setter
    def numero_identificacion(self, value):
        """Encriptar número de identificación"""
        if value:
            try:
                self._numero_identificacion_encrypted = encrypt_data(value)
            except EncryptionError as e:
                print(f"Error encriptando ID: {e}")
        else:
            self._numero_identificacion_encrypted = None


# Ejemplo 2: Uso en vistas o servicios
def ejemplo_uso_encriptacion():
    """
    Ejemplo de cómo usar la encriptación en vistas o servicios.
    """
    from utils import encrypt_data, decrypt_data, InvalidCiphertextError
    
    # Encriptar datos sensibles
    email_original = "usuario@ejemplo.com"
    email_encriptado = encrypt_data(email_original)
    print(f"Email original: {email_original}")
    print(f"Email encriptado: {email_encriptado}")
    
    # Desencriptar datos
    try:
        email_desencriptado = decrypt_data(email_encriptado)
        print(f"Email desencriptado: {email_desencriptado}")
    except InvalidCiphertextError:
        print("Error: Los datos pueden estar alterados o la clave es incorrecta")
    
    # Intentar desencriptar datos alterados (fallará)
    datos_alterados = email_encriptado[:-5] + "xxxxx"
    try:
        decrypt_data(datos_alterados)
    except InvalidCiphertextError as e:
        print(f"Verificación de integridad fallida: {e}")


# Ejemplo 3: Encriptación en serializers DRF (Django REST Framework)
def ejemplo_serializer_rest():
    """
    Ejemplo de cómo usar encriptación en serializers REST.
    """
    from rest_framework import serializers
    from utils import encrypt_data, decrypt_data
    
    class PersonaSerializer(serializers.Serializer):
        nombre = serializers.CharField()
        email = serializers.EmailField()
        numero_identificacion = serializers.CharField()
        
        def to_representation(self, instance):
            """Encriptar datos al enviar al cliente"""
            data = super().to_representation(instance)
            # Opcional: encriptar datos sensibles antes de enviar
            # data['email'] = encrypt_data(data['email'])
            return data
        
        def to_internal_value(self, data):
            """Desencriptar datos recibidos del cliente"""
            # Opcional: desencriptar datos recibidos
            # if 'email_encrypted' in data:
            #     data['email'] = decrypt_data(data['email_encrypted'])
            return super().to_internal_value(data)


if __name__ == "__main__":
    ejemplo_uso_encriptacion()
