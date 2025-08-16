import pytest
from fastapi.testclient import TestClient
from main import app
from models import UserRegistration

client = TestClient(app)

def test_registro_usuario_valido():
    """Prueba registro de usuario con datos válidos"""
    user_data = {
        "nombre": "María González López",
        "email": "maria.gonzalez@ejemplo.com",
        "edad": 28
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["nombre"] == user_data["nombre"]
    assert data["email"] == user_data["email"]
    assert data["edad"] == user_data["edad"]
    assert "id" in data
    assert "fecha_registro" in data

def test_registro_nombre_invalido():
    """Prueba registro con nombre inválido"""
    user_data = {
        "nombre": "Juan",  # Solo un nombre, falta apellido
        "email": "juan@ejemplo.com",
        "edad": 25
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 422

def test_registro_nombre_con_numeros():
    """Prueba registro con nombre que contiene números"""
    user_data = {
        "nombre": "Juan123 Pérez",
        "email": "juan@ejemplo.com",
        "edad": 25
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 422

def test_registro_email_invalido():
    """Prueba registro con email inválido"""
    user_data = {
        "nombre": "Ana Martínez",
        "email": "email_invalido",
        "edad": 30
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 422

def test_registro_email_temporal():
    """Prueba registro con email temporal/desechable"""
    user_data = {
        "nombre": "Carlos Ruiz",
        "email": "carlos@10minutemail.com",
        "edad": 35
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 422

def test_registro_edad_menor_13():
    """Prueba registro con edad menor a 13 años"""
    user_data = {
        "nombre": "Pedro Sánchez",
        "email": "pedro@ejemplo.com",
        "edad": 12
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 422

def test_registro_edad_mayor_120():
    """Prueba registro con edad mayor a 120 años"""
    user_data = {
        "nombre": "Elena Torres",
        "email": "elena@ejemplo.com",
        "edad": 125
    }
    
    response = client.post("/api/usuarios/registrar", json=user_data)
    assert response.status_code == 422

def test_registro_email_duplicado():
    """Prueba registro con email ya existente"""
    # Primer registro
    user_data1 = {
        "nombre": "Luis Morales",
        "email": "luis@ejemplo.com",
        "edad": 40
    }
    
    response1 = client.post("/api/usuarios/registrar", json=user_data1)
    assert response1.status_code == 201
    
    # Segundo registro con mismo email
    user_data2 = {
        "nombre": "Luis Morales Jr",
        "email": "luis@ejemplo.com",
        "edad": 18
    }
    
    response2 = client.post("/api/usuarios/registrar", json=user_data2)
    assert response2.status_code == 409

def test_listar_usuarios():
    """Prueba listar usuarios registrados"""
    response = client.get("/api/usuarios")
    assert response.status_code == 200
    
    data = response.json()
    assert "usuarios" in data
    assert "total" in data
    assert isinstance(data["usuarios"], list)
    assert isinstance(data["total"], int)

def test_obtener_usuario_por_id():
    """Prueba obtener usuario por ID"""
    # Primero registrar un usuario
    user_data = {
        "nombre": "Isabel Castro",
        "email": "isabel@ejemplo.com",
        "edad": 32
    }
    
    response_registro = client.post("/api/usuarios/registrar", json=user_data)
    assert response_registro.status_code == 201
    
    user_id = response_registro.json()["id"]
    
    # Luego obtener el usuario por ID
    response_obtener = client.get(f"/api/usuarios/{user_id}")
    assert response_obtener.status_code == 200
    
    data = response_obtener.json()
    assert data["nombre"] == user_data["nombre"]
    assert data["email"] == user_data["email"]
    assert data["edad"] == user_data["edad"]

def test_obtener_usuario_inexistente():
    """Prueba obtener usuario con ID inexistente"""
    response = client.get("/api/usuarios/usuario_inexistente")
    assert response.status_code == 404

def test_endpoint_raiz():
    """Prueba endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    
    data = response.json()
    assert "mensaje" in data
    assert "version" in data
    assert "endpoints" in data

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
