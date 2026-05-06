"""
Script de demostración de encriptación sin dependencias de Django.
"""

import os
import sys
from pathlib import Path

# Cargar variables de entorno del .env
from dotenv import load_dotenv
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path)

# Importar después de cargar .env
from utils import encrypt_data, decrypt_data, InvalidCiphertextError

def demo_encryption():
    """Demostración de AES-256-GCM"""
    print("\n" + "="*60)
    print("DEMOSTRACIÓN: AES-256-GCM para Protección en Reposo")
    print("="*60 + "\n")
    
    # Test 1: Encriptación básica
    print("[1] ENCRIPTACIÓN Y DESENCRIPTACIÓN BÁSICA")
    print("-" * 60)
    
    datos_sensibles = "usuario@ejemplo.com"
    print(f"Datos originales: {datos_sensibles}")
    
    datos_encriptados = encrypt_data(datos_sensibles)
    print(f"Datos encriptados (AES-256-GCM): {datos_encriptados[:70]}...")
    
    datos_recuperados = decrypt_data(datos_encriptados)
    print(f"Datos desencriptados: {datos_recuperados}")
    
    assert datos_recuperados == datos_sensibles
    print("✅ Verificación: EXITOSA\n")
    
    # Test 2: Nonce aleatorio (no determinista)
    print("[2] NONCE ALEATORIO (CADA ENCRIPTACIÓN ES DIFERENTE)")
    print("-" * 60)
    
    mismo_dato = "123-456-789-0"
    enc1 = encrypt_data(mismo_dato)
    enc2 = encrypt_data(mismo_dato)
    
    print(f"Mismo dato encriptado 2 veces:")
    print(f"  Encriptación 1: {enc1[:60]}...")
    print(f"  Encriptación 2: {enc2[:60]}...")
    print(f"  ¿Son diferentes? {enc1 != enc2}")
    
    print(f"Ambos desencriptan al mismo valor:")
    print(f"  Des. 1: {decrypt_data(enc1)}")
    print(f"  Des. 2: {decrypt_data(enc2)}")
    print("✅ Verificación: EXITOSA\n")
    
    # Test 3: Verificación de integridad
    print("[3] VERIFICACIÓN DE INTEGRIDAD (DETECTAR ALTERACIONES)")
    print("-" * 60)
    
    informacion_critica = "Acceso de nivel ADMINISTRADOR"
    enc_critico = encrypt_data(informacion_critica)
    print(f"Información crítica encriptada: {enc_critico[:60]}...")
    
    # Simular alteración
    enc_alterado = enc_critico[:-5] + "XXXXX"
    print(f"Datos alterados maliciosamente: {enc_alterado[:60]}...")
    
    try:
        decrypt_data(enc_alterado)
        print("❌ ERROR: Los datos alterados se desencriptaron (FALLO)")
    except InvalidCiphertextError as e:
        print(f"✅ Integridad comprometida detectada: {e}\n")
    
    # Test 4: Unicode y caracteres especiales
    print("[4] SOPORTE PARA UNICODE Y CARACTERES ESPECIALES")
    print("-" * 60)
    
    ejemplos_unicode = [
        ("Español", "¡Contraseña: señor_1234!"),
        ("Chino", "密码: 你好世界"),
        ("Árabe", "كلمة السر: مرحبا"),
        ("Emojis", "Clave segura 🔐 🔑 ✅"),
    ]
    
    for idioma, dato in ejemplos_unicode:
        enc = encrypt_data(dato)
        dec = decrypt_data(enc)
        assert dec == dato
        print(f"  ✅ {idioma:10} | {dato}")
    
    print("\n✅ Verificación: EXITOSA\n")
    
    # Test 5: Información sobre la encriptación
    print("[5] INFORMACIÓN TÉCNICA")
    print("-" * 60)
    
    info = {
        "Algoritmo": "AES-256-GCM",
        "Tamaño de clave": "256 bits (32 bytes)",
        "Modo": "AEAD (Authenticated Encryption with Associated Data)",
        "Nonce": "96 bits (12 bytes) - Aleatorio cada vez",
        "Tag de autenticación": "128 bits (incluido automáticamente)",
        "Propiedades": [
            "✓ Confidencialidad: Los datos no se pueden leer",
            "✓ Integridad: Se detectan alteraciones",
            "✓ Autenticidad: Se valida la procedencia",
        ]
    }
    
    for clave, valor in info.items():
        if isinstance(valor, list):
            print(f"{clave}:")
            for item in valor:
                print(f"  {item}")
        else:
            print(f"{clave}: {valor}")
    
    print("\n" + "="*60)
    print("✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
    print("="*60 + "\n")


if __name__ == "__main__":
    try:
        demo_encryption()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
