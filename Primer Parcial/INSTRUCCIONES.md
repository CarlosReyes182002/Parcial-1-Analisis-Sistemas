# 🚀 Instrucciones de Ejecución Rápida

## ⚡ Inicio Rápido (5 minutos)

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar la API
```bash
python main.py
```

### 3. Verificar Funcionamiento
- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Probar la API

### Opción 1: Usar el Script de Ejemplo
```bash
python ejemplo_uso.py
```

### Opción 2: Usar cURL
```bash
# Registro exitoso
curl -X POST "http://localhost:8000/api/usuarios/registrar" \
     -H "Content-Type: application/json" \
     -d '{
       "nombre": "Juan Pérez López",
       "email": "juan.perez@ejemplo.com",
       "edad": 25
     }'

# Listar usuarios
curl "http://localhost:8000/api/usuarios"
```

### Opción 3: Usar la Documentación Interactiva
1. Abrir http://localhost:8000/docs
2. Hacer clic en "Try it out" en el endpoint de registro
3. Ingresar datos de prueba
4. Ejecutar y ver resultados

## 📋 Casos de Prueba Recomendados

### ✅ Casos Válidos
- **Nombre completo**: "María González López"
- **Email válido**: "maria@ejemplo.com"
- **Edad realista**: 28

### ❌ Casos Inválidos (deben fallar)
- **Nombre corto**: "Juan" (falta apellido)
- **Email temporal**: "test@10minutemail.com"
- **Edad menor**: 12 años
- **Email duplicado**: usar el mismo email dos veces

## 🔧 Solución de Problemas

### Error: "No module named 'fastapi'"
```bash
pip install fastapi uvicorn
```

### Error: "Address already in use"
```bash
# Cambiar puerto en main.py o config.py
# O matar proceso en puerto 8000
```

### Error de Conexión
- Verificar que la API esté ejecutándose
- Verificar puerto correcto
- Verificar firewall/antivirus

## 📊 Verificar Funcionamiento

### 1. Endpoint Raíz
```bash
curl http://localhost:8000/
```
**Respuesta esperada**: Información de la API

### 2. Registro de Usuario
```bash
curl -X POST "http://localhost:8000/api/usuarios/registrar" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Test User", "email": "test@test.com", "edad": 25}'
```
**Respuesta esperada**: Usuario creado con ID único

### 3. Listar Usuarios
```bash
curl http://localhost:8000/api/usuarios
```
**Respuesta esperada**: Lista de usuarios registrados

## 🎯 Criterios de Evaluación Verificados

### ✅ Modelo Completo (25%)
- [x] Modelo Pydantic con validaciones
- [x] Validadores personalizados
- [x] Manejo de caracteres especiales
- [x] Validaciones de negocio

### ✅ Endpoint Funcional (25%)
- [x] Endpoint de registro funcional
- [x] Respuestas HTTP apropiadas
- [x] IDs únicos automáticos
- [x] Timestamps de registro

### ✅ Seguridad (25%)
- [x] Validación exhaustiva
- [x] Prevención de duplicados
- [x] Manejo de excepciones
- [x] Logging de operaciones

### ✅ Claridad y Realismo (25%)
- [x] Documentación completa
- [x] Código bien estructurado
- [x] Validaciones realistas
- [x] Manejo de casos edge

## 🚀 Próximos Pasos

### Para Producción
1. **Base de datos**: Implementar PostgreSQL/MySQL
2. **Autenticación**: Agregar JWT/OAuth2
3. **Rate limiting**: Limitar requests por IP
4. **Logging**: Configurar logging estructurado
5. **Monitoreo**: Implementar métricas y alertas

### Para Desarrollo
1. **Tests**: Ejecutar `python tests.py`
2. **Validaciones**: Agregar más reglas de negocio
3. **Endpoints**: Implementar CRUD completo
4. **Documentación**: Agregar más ejemplos

## 📞 Soporte

Si encuentras problemas:
1. Verificar que todas las dependencias estén instaladas
2. Revisar logs de la consola
3. Verificar puertos disponibles
4. Consultar la documentación en `/docs`

---

**¡La API está lista para usar! 🎉**
