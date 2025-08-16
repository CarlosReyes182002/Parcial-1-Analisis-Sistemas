from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import uuid
from datetime import datetime
import logging
from typing import Dict, Any

from models import UserRegistration, UserResponse, ErrorResponse

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API de Validación de Usuarios",
    description="API para validar y registrar usuarios con validaciones robustas",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Almacenamiento en memoria (en producción usar base de datos)
users_db: Dict[str, Dict[str, Any]] = {}

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Manejar errores de validación de Pydantic"""
    logger.warning(f"Error de validación: {exc.errors()}")
    
    error_response = ErrorResponse(
        error="Error de validación",
        detalle="Los datos proporcionados no cumplen con los requisitos",
        codigo_error="VALIDATION_ERROR",
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=422,
        content=error_response.dict()
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Manejar excepciones HTTP personalizadas"""
    logger.error(f"Error HTTP {exc.status_code}: {exc.detail}")
    
    error_response = ErrorResponse(
        error=exc.detail,
        detalle="Ocurrió un error en el servidor",
        codigo_error=f"HTTP_{exc.status_code}",
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Manejar excepciones generales no capturadas"""
    logger.error(f"Error no manejado: {str(exc)}", exc_info=True)
    
    error_response = ErrorResponse(
        error="Error interno del servidor",
        detalle="Ocurrió un error inesperado",
        codigo_error="INTERNAL_ERROR",
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )

@app.post("/api/usuarios/registrar", 
          response_model=UserResponse,
          status_code=201,
          summary="Registrar nuevo usuario",
          description="Endpoint para registrar un nuevo usuario con validaciones robustas")
async def registrar_usuario(user_data: UserRegistration):
    """
    Registra un nuevo usuario con las siguientes validaciones:
    
    - **Nombre**: Debe contener al menos nombre y apellido, solo letras y espacios
    - **Email**: Debe ser un email válido y no temporal/desechable
    - **Edad**: Debe estar entre 13 y 120 años
    
    Retorna los datos del usuario registrado o un error de validación.
    """
    try:
        # Verificar si el email ya existe
        if any(user["email"] == user_data.email for user in users_db.values()):
            raise HTTPException(
                status_code=409,
                detail="El email ya está registrado en el sistema"
            )
        
        # Generar ID único
        user_id = str(uuid.uuid4())
        fecha_registro = datetime.now().isoformat()
        
        # Crear usuario
        user_dict = {
            "id": user_id,
            "nombre": user_data.nombre,
            "email": user_data.email,
            "edad": user_data.edad,
            "fecha_registro": fecha_registro
        }
        
        # Guardar en "base de datos"
        users_db[user_id] = user_dict
        
        logger.info(f"Usuario registrado exitosamente: {user_data.email}")
        
        return UserResponse(
            id=user_id,
            nombre=user_data.nombre,
            email=user_data.email,
            edad=user_data.edad,
            fecha_registro=fecha_registro
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al registrar usuario: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al procesar el registro"
        )

@app.get("/api/usuarios", 
         summary="Listar usuarios",
         description="Endpoint para listar todos los usuarios registrados")
async def listar_usuarios():
    """Lista todos los usuarios registrados en el sistema"""
    try:
        return {
            "usuarios": list(users_db.values()),
            "total": len(users_db)
        }
    except Exception as e:
        logger.error(f"Error al listar usuarios: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al listar usuarios"
        )

@app.get("/api/usuarios/{user_id}", 
         summary="Obtener usuario por ID",
         description="Endpoint para obtener un usuario específico por su ID")
async def obtener_usuario(user_id: str):
    """Obtiene un usuario específico por su ID"""
    try:
        if user_id not in users_db:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado"
            )
        
        return users_db[user_id]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al obtener usuario {user_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor al obtener usuario"
        )

@app.get("/", summary="Información de la API")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "API de Validación de Usuarios",
        "version": "1.0.0",
        "endpoints": {
            "registro": "/api/usuarios/registrar",
            "listar": "/api/usuarios",
            "obtener": "/api/usuarios/{user_id}",
            "documentacion": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
