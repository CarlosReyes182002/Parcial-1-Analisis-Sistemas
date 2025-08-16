"""
Configuración de la API de Validación de Usuarios
Archivo centralizado para configuraciones de seguridad, validación y comportamiento
"""

import os
from typing import List

class Settings:
    """Configuraciones de la aplicación"""
    
    # Configuración básica
    APP_NAME: str = "API de Validación de Usuarios"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Configuración del servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Configuración de CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React dev server
        "http://localhost:8080",  # Vue dev server
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
    ]
    
    # Configuración de validación de usuarios
    NOMBRE_MIN_LENGTH: int = 2
    NOMBRE_MAX_LENGTH: int = 50
    EDAD_MINIMA: int = 13
    EDAD_MAXIMA: int = 120
    
    # Dominios de email bloqueados (temporales/desechables)
    DOMINIOS_BLOQUEADOS: List[str] = [
        "10minutemail.com",
        "tempmail.org", 
        "guerrillamail.com",
        "mailinator.com",
        "yopmail.com",
        "temp-mail.org",
        "sharklasers.com",
        "grr.la",
        "guerrillamailblock.com",
        "guerrillamail.net",
        "guerrillamail.org",
        "guerrillamailblock.com",
        "guerrillamail.net",
        "guerrillamail.org",
        "guerrillamailblock.com",
        "guerrillamail.net",
        "guerrillamail.org",
        "guerrillamailblock.com",
        "guerrillamail.net",
        "guerrillamail.org"
    ]
    
    # Configuración de logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configuración de seguridad
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_WINDOW: int = int(os.getenv("RATE_LIMIT_WINDOW", "3600"))  # 1 hora
    
    # Configuración de base de datos (para futuras implementaciones)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./usuarios.db")
    
    # Configuración de autenticación (para futuras implementaciones)
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Configuración de validación adicional
    EMAIL_VERIFICATION_REQUIRED: bool = os.getenv("EMAIL_VERIFICATION_REQUIRED", "False").lower() == "true"
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    
    # Configuración de monitoreo
    ENABLE_METRICS: bool = os.getenv("ENABLE_METRICS", "False").lower() == "true"
    METRICS_PORT: int = int(os.getenv("METRICS_PORT", "9090"))
    
    @classmethod
    def get_cors_origins(cls) -> List[str]:
        """Obtener orígenes CORS permitidos"""
        if cls.DEBUG:
            return ["*"]  # En desarrollo, permitir todos los orígenes
        return cls.CORS_ORIGINS
    
    @classmethod
    def get_dominios_bloqueados(cls) -> List[str]:
        """Obtener lista de dominios de email bloqueados"""
        return [dominio.lower() for dominio in cls.DOMINIOS_BLOQUEADOS]
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validar que la configuración sea correcta"""
        try:
            assert cls.PORT > 0 and cls.PORT < 65536, "Puerto inválido"
            assert cls.EDAD_MINIMA > 0, "Edad mínima debe ser mayor a 0"
            assert cls.EDAD_MAXIMA > cls.EDAD_MINIMA, "Edad máxima debe ser mayor a la mínima"
            assert cls.NOMBRE_MIN_LENGTH > 0, "Longitud mínima del nombre debe ser mayor a 0"
            assert cls.NOMBRE_MAX_LENGTH > cls.NOMBRE_MIN_LENGTH, "Longitud máxima debe ser mayor a la mínima"
            return True
        except AssertionError as e:
            print(f"❌ Error de configuración: {e}")
            return False

# Instancia global de configuración
settings = Settings()

# Validar configuración al importar
if not settings.validate_config():
    raise ValueError("Configuración inválida. Revisa los parámetros.")
