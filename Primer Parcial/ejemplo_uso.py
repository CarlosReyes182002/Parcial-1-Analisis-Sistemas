#!/usr/bin/env python3
"""
Ejemplo de uso de la API de Validación de Usuarios
Este script demuestra cómo usar la API para registrar usuarios y manejar diferentes escenarios
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:8000"
HEADERS = {"Content-Type": "application/json"}

def print_separator(title):
    """Imprimir separador visual"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_response(response, title):
    """Imprimir respuesta de la API de forma legible"""
    print(f"\n📡 {title}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")

def test_registro_exitoso():
    """Probar registro exitoso de usuario"""
    print_separator("REGISTRO EXITOSO")
    
    user_data = {
        "nombre": "Ana María Rodríguez López",
        "email": "ana.rodriguez@ejemplo.com",
        "edad": 29
    }
    
    print(f"📝 Intentando registrar usuario: {user_data['nombre']}")
    
    response = requests.post(
        f"{BASE_URL}/api/usuarios/registrar",
        json=user_data,
        headers=HEADERS
    )
    
    print_response(response, "Registro Exitoso")
    return response.json() if response.status_code == 201 else None

def test_validacion_nombre():
    """Probar validaciones de nombre"""
    print_separator("VALIDACIÓN DE NOMBRE")
    
    casos_prueba = [
        {
            "nombre": "Juan",  # Solo un nombre
            "email": "juan@ejemplo.com",
            "edad": 25,
            "descripcion": "Solo un nombre (debe fallar)"
        },
        {
            "nombre": "María123 López",  # Con números
            "email": "maria@ejemplo.com",
            "edad": 30,
            "descripcion": "Nombre con números (debe fallar)"
        },
        {
            "nombre": "   ",  # Solo espacios
            "email": "espacios@ejemplo.com",
            "edad": 35,
            "descripcion": "Solo espacios (debe fallar)"
        }
    ]
    
    for caso in casos_prueba:
        print(f"\n🔍 Probando: {caso['descripcion']}")
        print(f"   Datos: {caso}")
        
        response = requests.post(
            f"{BASE_URL}/api/usuarios/registrar",
            json=caso,
            headers=HEADERS
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code != 201:
            print(f"   Error: {response.json().get('error', 'Error desconocido')}")

def test_validacion_email():
    """Probar validaciones de email"""
    print_separator("VALIDACIÓN DE EMAIL")
    
    casos_prueba = [
        {
            "nombre": "Carlos Pérez",
            "email": "email_invalido",
            "edad": 28,
            "descripcion": "Email sin formato válido"
        },
        {
            "nombre": "Elena Torres",
            "email": "elena@10minutemail.com",
            "edad": 32,
            "descripcion": "Email temporal/desechable"
        },
        {
            "nombre": "Luis Morales",
            "email": "luis@mailinator.com",
            "edad": 40,
            "descripcion": "Otro email temporal"
        }
    ]
    
    for caso in casos_prueba:
        print(f"\n🔍 Probando: {caso['descripcion']}")
        print(f"   Datos: {caso}")
        
        response = requests.post(
            f"{BASE_URL}/api/usuarios/registrar",
            json=caso,
            headers=HEADERS
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code != 201:
            print(f"   Error: {response.json().get('error', 'Error desconocido')}")

def test_validacion_edad():
    """Probar validaciones de edad"""
    print_separator("VALIDACIÓN DE EDAD")
    
    casos_prueba = [
        {
            "nombre": "Pedro Sánchez",
            "email": "pedro@ejemplo.com",
            "edad": 12,
            "descripcion": "Edad menor a 13 años"
        },
        {
            "nombre": "Isabel Castro",
            "email": "isabel@ejemplo.com",
            "edad": 125,
            "descripcion": "Edad mayor a 120 años"
        },
        {
            "nombre": "Roberto Díaz",
            "email": "roberto@ejemplo.com",
            "edad": -5,
            "descripcion": "Edad negativa"
        }
    ]
    
    for caso in casos_prueba:
        print(f"\n🔍 Probando: {caso['descripcion']}")
        print(f"   Datos: {caso}")
        
        response = requests.post(
            f"{BASE_URL}/api/usuarios/registrar",
            json=caso,
            headers=HEADERS
        )
        
        print(f"   Status: {response.status_code}")
        if response.status_code != 201:
            print(f"   Error: {response.json().get('error', 'Error desconocido')}")

def test_email_duplicado():
    """Probar prevención de emails duplicados"""
    print_separator("PREVENCIÓN DE EMAILS DUPLICADOS")
    
    # Primer registro
    user_data = {
        "nombre": "Mónica Vega",
        "email": "monica.vega@ejemplo.com",
        "edad": 27
    }
    
    print("📝 Registrando primer usuario...")
    response1 = requests.post(
        f"{BASE_URL}/api/usuarios/registrar",
        json=user_data,
        headers=HEADERS
    )
    
    if response1.status_code == 201:
        print("✅ Primer usuario registrado exitosamente")
        
        # Intentar registrar con mismo email
        user_data2 = {
            "nombre": "Mónica Vega Jr",
            "email": "monica.vega@ejemplo.com",  # Mismo email
            "edad": 5
        }
        
        print("📝 Intentando registrar segundo usuario con mismo email...")
        response2 = requests.post(
            f"{BASE_URL}/api/usuarios/registrar",
            json=user_data2,
            headers=HEADERS
        )
        
        print_response(response2, "Prevención de Duplicado")
    else:
        print(f"❌ Error al registrar primer usuario: {response1.status_code}")

def test_endpoints_adicionales():
    """Probar endpoints adicionales"""
    print_separator("ENDPOINTS ADICIONALES")
    
    # Listar usuarios
    print("📋 Listando todos los usuarios...")
    response = requests.get(f"{BASE_URL}/api/usuarios")
    print_response(response, "Lista de Usuarios")
    
    # Información de la API
    print("\n📚 Obteniendo información de la API...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Información de la API")

def main():
    """Función principal que ejecuta todas las pruebas"""
    print("🚀 INICIANDO DEMOSTRACIÓN DE LA API DE VALIDACIÓN DE USUARIOS")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Verificar que la API esté funcionando
        print("\n🔍 Verificando conectividad con la API...")
        response = requests.get(f"{BASE_URL}/")
        
        if response.status_code != 200:
            print(f"❌ Error: No se puede conectar a la API en {BASE_URL}")
            print("   Asegúrate de que la API esté ejecutándose con: python main.py")
            return
        
        print("✅ API conectada exitosamente")
        
        # Ejecutar todas las pruebas
        test_registro_exitoso()
        test_validacion_nombre()
        test_validacion_email()
        test_validacion_edad()
        test_email_duplicado()
        test_endpoints_adicionales()
        
        print_separator("DEMOSTRACIÓN COMPLETADA")
        print("🎉 Todas las pruebas han sido ejecutadas")
        print("📖 Revisa la documentación en: http://localhost:8000/docs")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Error de conexión: No se puede conectar a {BASE_URL}")
        print("   Asegúrate de que la API esté ejecutándose")
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()
