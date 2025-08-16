from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import re

class UserRegistration(BaseModel):
    """
    Modelo para registro de usuarios con validaciones robustas
    """
    nombre: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre completo del usuario",
        example="Juan Carlos Pérez"
    )
    
    email: EmailStr = Field(
        ...,
        description="Correo electrónico válido",
        example="juan.perez@ejemplo.com"
    )
    
    edad: int = Field(
        ...,
        ge=13,
        le=120,
        description="Edad del usuario (entre 13 y 120 años)",
        example=25
    )
    
    @validator('nombre')
    def validate_nombre(cls, v):
        """Validar que el nombre contenga solo letras, espacios y caracteres especiales válidos"""
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', v):
            raise ValueError('El nombre solo puede contener letras, espacios y caracteres especiales del español')
        
        # Verificar que no sea solo espacios
        if v.strip() == '':
            raise ValueError('El nombre no puede estar vacío o contener solo espacios')
        
        # Verificar que tenga al menos dos palabras (nombre y apellido)
        palabras = [palabra for palabra in v.split() if palabra.strip()]
        if len(palabras) < 2:
            raise ValueError('El nombre debe incluir al menos nombre y apellido')
        
        return v.strip()
    
    @validator('email')
    def validate_email_domain(cls, v):
        """Validar dominio del email y formato adicional"""
        # Verificar que no sea un email temporal o desechable
        dominios_temporales = [
            '10minutemail.com', 'tempmail.org', 'guerrillamail.com',
            'mailinator.com', 'yopmail.com', 'temp-mail.org'
        ]
        
        dominio = v.split('@')[1].lower()
        if dominio in dominios_temporales:
            raise ValueError('No se permiten emails temporales o desechables')
        
        return v.lower()
    
    @validator('edad')
    def validate_edad_realista(cls, v):
        """Validar que la edad sea realista para el contexto"""
        if v < 13:
            raise ValueError('Debes tener al menos 13 años para registrarte')
        if v > 120:
            raise ValueError('La edad proporcionada no es realista')
        
        return v

class UserResponse(BaseModel):
    """Modelo de respuesta para usuarios registrados exitosamente"""
    id: str
    nombre: str
    email: str
    edad: int
    fecha_registro: str
    mensaje: str = "Usuario registrado exitosamente"

class ErrorResponse(BaseModel):
    """Modelo para respuestas de error estandarizadas"""
    error: str
    detalle: str
    codigo_error: str
    timestamp: str
