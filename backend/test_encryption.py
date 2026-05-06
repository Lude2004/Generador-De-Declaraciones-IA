"""
Pruebas unitarias para la encriptación AES-256-GCM.
Ejecutar con: python manage.py test core.tests.test_encryption
o: python -m pytest test_encryption.py
"""

import os
try:
    import pytest
except ImportError:
    pytest = None

from utils import (
    encrypt_data,
    decrypt_data,
    EncryptionError,
    InvalidCiphertextError,
    EncryptionKeyError,
    _get_encryption_key,
)


class TestAESGCMEncryption:
    """Suite de pruebas para AES-256-GCM"""
    
    def setup_method(self):
        """Setup: Verificar que la clave de encriptación está configurada"""
        if pytest is None:
            return
        if not os.getenv("ENCRYPTION_KEY"):
            pytest.skip("ENCRYPTION_KEY no configurada")
    
    def test_encrypt_decrypt_roundtrip(self):
        """Prueba: Encriptar y desencriptar texto debe recuperar el original"""
        texto_original = "Este es un texto sensible para encriptar"
        
        # Encriptar
        ciphertext = encrypt_data(texto_original)
        assert ciphertext != texto_original
        assert len(ciphertext) > 0
        
        # Desencriptar
        texto_recuperado = decrypt_data(ciphertext)
        assert texto_recuperado == texto_original
    
    def test_encrypt_produces_different_output(self):
        """Prueba: Encriptar el mismo texto dos veces produce resultados diferentes (nonce aleatorio)"""
        texto = "Prueba de nonce aleatorio"
        
        ciphertext1 = encrypt_data(texto)
        ciphertext2 = encrypt_data(texto)
        
        # Los ciphertexts deben ser diferentes debido al nonce aleatorio
        assert ciphertext1 != ciphertext2
        
        # Ambos deben desencriptarse al texto original
        assert decrypt_data(ciphertext1) == texto
        assert decrypt_data(ciphertext2) == texto
    
    def test_decrypt_tampered_ciphertext(self):
        """Prueba: Desencriptar datos alterados debe fallar (verificación de integridad)"""
        if pytest is None:
            return
        texto_original = "Datos que serán alterados"
        ciphertext = encrypt_data(texto_original)
        
        # Alterar el ciphertext
        ciphertext_corrupto = ciphertext[:-5] + "XXXXX"
        
        # Desencriptar debe fallar
        with pytest.raises(InvalidCiphertextError):
            decrypt_data(ciphertext_corrupto)
    
    def test_decrypt_invalid_base64(self):
        """Prueba: Desencriptar base64 inválido debe fallar"""
        ciphertext_invalido = "¡Esto no es base64!"
        
        with pytest.raises(InvalidCiphertextError):
            decrypt_data(ciphertext_invalido)
    
    def test_decrypt_short_ciphertext(self):
        """Prueba: Desencriptar ciphertext muy corto debe fallar"""
        # Ciphertext válido en base64 pero demasiado corto
        ciphertext_corto = "YQ=="  # Solo 'a' en base64
        
        with pytest.raises(InvalidCiphertextError):
            decrypt_data(ciphertext_corto)
    
    def test_encrypt_unicode_text(self):
        """Prueba: Encriptar texto con caracteres Unicode"""
        textos_unicode = [
            "Español: ¡Hola, qué tal!",
            "中文: 你好世界",
            "Árabe: مرحبا بالعالم",
            "Emojis: 🔐 🔑 ✅",
        ]
        
        for texto in textos_unicode:
            ciphertext = encrypt_data(texto)
            texto_recuperado = decrypt_data(ciphertext)
            assert texto_recuperado == texto
    
    def test_encrypt_empty_string(self):
        """Prueba: Encriptar una cadena vacía"""
        texto_vacio = ""
        ciphertext = encrypt_data(texto_vacio)
        assert decrypt_data(ciphertext) == texto_vacio
    
    def test_encrypt_large_text(self):
        """Prueba: Encriptar texto grande (1MB)"""
        texto_grande = "x" * (1024 * 1024)  # 1MB
        ciphertext = encrypt_data(texto_grande)
        texto_recuperado = decrypt_data(ciphertext)
        assert texto_recuperado == texto_grande
        assert len(ciphertext) > len(texto_grande)
    
    def test_encrypt_non_string_input(self):
        """Prueba: Encriptar no-string debe fallar"""
        with pytest.raises(EncryptionError):
            encrypt_data(12345)
        
        with pytest.raises(EncryptionError):
            encrypt_data(None)
        
        with pytest.raises(EncryptionError):
            encrypt_data({"key": "value"})
    
    def test_decrypt_non_string_input(self):
        """Prueba: Desencriptar no-string debe fallar"""
        with pytest.raises(InvalidCiphertextError):
            decrypt_data(12345)
        
        with pytest.raises(InvalidCiphertextError):
            decrypt_data(None)
    
    def test_get_encryption_key_success(self):
        """Prueba: Obtener clave de encriptación correctamente"""
        key = _get_encryption_key()
        assert isinstance(key, bytes)
        assert len(key) == 32  # 256 bits
    
    def test_get_encryption_key_missing_env(self):
        """Prueba: Obtener clave cuando falta en env debe fallar"""
        original_key = os.environ.get("ENCRYPTION_KEY")
        try:
            if "ENCRYPTION_KEY" in os.environ:
                del os.environ["ENCRYPTION_KEY"]
            
            with pytest.raises(EncryptionKeyError) as exc_info:
                _get_encryption_key()
            
            assert "ENCRYPTION_KEY no configurada" in str(exc_info.value)
        finally:
            if original_key:
                os.environ["ENCRYPTION_KEY"] = original_key
    
    def test_get_encryption_key_invalid_base64(self):
        """Prueba: Obtener clave con base64 inválido debe fallar"""
        original_key = os.environ.get("ENCRYPTION_KEY")
        try:
            os.environ["ENCRYPTION_KEY"] = "¡Esto no es base64!"
            
            with pytest.raises(EncryptionKeyError):
                _get_encryption_key()
        finally:
            if original_key:
                os.environ["ENCRYPTION_KEY"] = original_key
    
    def test_get_encryption_key_wrong_length(self):
        """Prueba: Obtener clave con longitud incorrecta debe fallar"""
        import base64
        original_key = os.environ.get("ENCRYPTION_KEY")
        try:
            # Crear clave de 128 bits en lugar de 256
            short_key = base64.urlsafe_b64encode(os.urandom(16)).decode()
            os.environ["ENCRYPTION_KEY"] = short_key
            
            with pytest.raises(EncryptionKeyError) as exc_info:
                _get_encryption_key()
            
            assert "256 bits" in str(exc_info.value)
        finally:
            if original_key:
                os.environ["ENCRYPTION_KEY"] = original_key


# Pruebas simples sin pytest (para ejecutar directamente)
def test_simple():
    """Prueba simple sin dependencias de pytest"""
    print("\n=== Prueba Simple de Encriptación AES-256-GCM ===\n")
    
    # Test 1: Roundtrip
    print("[1] Encriptación y Desencriptación:")
    texto = "Información Sensible"
    enc = encrypt_data(texto)
    dec = decrypt_data(enc)
    assert dec == texto
    print(f"  ✓ Original: {texto}")
    print(f"  ✓ Encriptado: {enc[:50]}...")
    print(f"  ✓ Desencriptado: {dec}\n")
    
    # Test 2: Nonce aleatorio
    print("[2] Nonce Aleatorio (Same text, different output):")
    enc1 = encrypt_data(texto)
    enc2 = encrypt_data(texto)
    assert enc1 != enc2
    assert decrypt_data(enc1) == decrypt_data(enc2) == texto
    print(f"  ✓ Salida 1: {enc1[:50]}...")
    print(f"  ✓ Salida 2: {enc2[:50]}...")
    print(f"  ✓ Ambas desencriptan al original\n")
    
    # Test 3: Integridad
    print("[3] Verificación de Integridad:")
    enc = encrypt_data("Datos importantes")
    enc_corrupto = enc[:-5] + "XXXXX"
    try:
        decrypt_data(enc_corrupto)
        print("  ✗ ERROR: Debería haber fallado")
    except InvalidCiphertextError as e:
        print(f"  ✓ Detectados datos alterados: {e}\n")
    
    # Test 4: Unicode
    print("[4] Soporte Unicode:")
    textos = ["Español ¡Hola!", "中文: 你好", "Emojis: 🔐"]
    for t in textos:
        assert decrypt_data(encrypt_data(t)) == t
        print(f"  ✓ {t}")
    print()
    
    print("✅ Todas las pruebas pasaron correctamente\n")


if __name__ == "__main__":
    test_simple()
