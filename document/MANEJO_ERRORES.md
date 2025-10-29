# Manejo de Errores y Casos Edge
**Sistema de Predicción de Morosidad - Ahorro Valle**

---

## Tabla de Contenidos

1. [Tipos de Errores](#tipos-de-errores)
2. [Validación de Datos](#validación-de-datos)
3. [Casos Edge Identificados](#casos-edge-identificados)
4. [Estrategias de Recuperación](#estrategias-de-recuperación)
5. [Logging y Monitoreo](#logging-y-monitoreo)
6. [Códigos de Error](#códigos-de-error)
7. [Procedimientos de Emergencia](#procedimientos-de-emergencia)

---

## Tipos de Errores

### 1. Errores de Validación de Entrada

#### Campos Faltantes
```python
ERROR_CAMPOS_FALTANTES = {
    "error": "validation_error",
    "message": "Campos requeridos faltantes",
    "missing_fields": ["edad", "ingresos_mensuales"],
    "code": "E001"
}
```

#### Tipos de Datos Incorrectos
```python
ERROR_TIPO_DATO = {
    "error": "data_type_error", 
    "message": "Tipo de dato incorrecto",
    "field": "edad",
    "expected": "int",
    "received": "string",
    "code": "E002"
}
```

#### Valores Fuera de Rango
```python
ERROR_RANGO = {
    "error": "range_error",
    "message": "Valor fuera del rango permitido",
    "field": "edad",
    "value": 150,
    "valid_range": "18-80",
    "code": "E003"
}
```

### 2. Errores del Sistema

#### Modelo No Disponible
```python
ERROR_MODELO = {
    "error": "model_error",
    "message": "Modelo de predicción no disponible",
    "code": "E101",
    "action": "Contactar soporte técnico"
}
```

#### Memoria Insuficiente
```python
ERROR_MEMORIA = {
    "error": "system_error",
    "message": "Memoria insuficiente para procesar la solicitud",
    "code": "E102",
    "retry_after": 60
}
```

---

## Validación de Datos

### Validación Frontend (JavaScript)
```javascript
function validarFormulario(datos) {
    const errores = [];
    
    // Validar edad
    if (!datos.edad || datos.edad < 18 || datos.edad > 80) {
        errores.push('Edad debe estar entre 18 y 80 años');
    }
    
    // Validar ingresos
    if (!datos.ingresos_mensuales || datos.ingresos_mensuales <= 0) {
        errores.push('Ingresos mensuales deben ser mayor a 0');
    }
    
    // Validar monto de crédito
    if (!datos.monto_credito || datos.monto_credito <= 0) {
        errores.push('Monto de crédito debe ser mayor a 0');
    }
    
    return {
        valido: errores.length === 0,
        errores: errores
    };
}
```

### Validación Backend (Python)
```python
def validar_datos_entrada(datos):
    errores = []
    
    # Campos requeridos
    campos_requeridos = [
        'edad', 'ingresos_mensuales', 'monto_credito', 
        'plazo_meses', 'credito_score'
    ]
    
    for campo in campos_requeridos:
        if campo not in datos or datos[campo] is None:
            errores.append(f"Campo requerido faltante: {campo}")
    
    # Validaciones específicas
    if 'edad' in datos:
        if not isinstance(datos['edad'], (int, float)) or datos['edad'] < 18 or datos['edad'] > 80:
            errores.append("Edad debe ser un número entre 18 y 80")
    
    if 'ingresos_mensuales' in datos:
        if not isinstance(datos['ingresos_mensuales'], (int, float)) or datos['ingresos_mensuales'] <= 0:
            errores.append("Ingresos mensuales debe ser un número positivo")
    
    if 'credito_score' in datos:
        if not isinstance(datos['credito_score'], (int, float)) or datos['credito_score'] < 300 or datos['credito_score'] > 850:
            errores.append("Credit score debe estar entre 300 y 850")
    
    return {
        'valido': len(errores) == 0,
        'errores': errores
    }
```

---

## Casos Edge Identificados

### 1. Datos Extremos Válidos

| Campo | Valor Mínimo | Valor Máximo | Comportamiento |
|-------|--------------|--------------|----------------|
| Edad | 18 años | 80 años | Procesamiento normal |
| Ingresos | $1,000,000 | $50,000,000 | Advertencia si >$20M |
| Crédito Score | 300 | 850 | Normal |
| Plazo | 1 mes | 120 meses | Normal |

### 2. Combinaciones Atípicas

#### Cliente Joven con Ingresos Altos
- **Escenario**: Edad 22, ingresos $15,000,000
- **Comportamiento**: Predicción normal con advertencia de revisión manual

#### Primer Crédito en Edad Avanzada  
- **Escenario**: Edad 65, sin historial crediticio
- **Comportamiento**: Mayor peso a ingresos y garantías

#### Crédito Pequeño con Ingresos Altos
- **Escenario**: Ingresos $10M, crédito $500,000
- **Comportamiento**: Bajo riesgo automático

### 3. Múltiples Usuarios Simultáneos
- **Límite**: 10 predicciones simultáneas
- **Rate Limiting**: 5 requests por minuto por IP
- **Cola de espera**: Timeout 30 segundos

---

## Estrategias de Recuperación

### 1. Auto-Recuperación
```python
def intentar_prediccion_con_reintentos(datos, max_intentos=3):
    for intento in range(max_intentos):
        try:
            return realizar_prediccion(datos)
        except MemoryError:
            if intento < max_intentos - 1:
                liberar_memoria_cache()
                time.sleep(2 ** intento)  # Backoff exponencial
            else:
                raise
        except ModeloNoDisponibleError:
            if intento < max_intentos - 1:
                recargar_modelo()
                time.sleep(1)
            else:
                return usar_prediccion_heuristica(datos)
```

### 2. Degradación Gradual
```python
def prediccion_con_degradacion(datos):
    try:
        # Intento 1: Predicción completa
        return prediccion_completa(datos)
    except Exception:
        try:
            # Intento 2: Predicción simplificada
            return prediccion_simplificada(datos)
        except Exception:
            # Último recurso: Reglas heurísticas
            return prediccion_heuristica(datos)
```

### 3. Circuit Breaker
```python
class CircuitBreaker:
    def __init__(self, umbral_fallos=5, tiempo_espera=60):
        self.fallos = 0
        self.umbral_fallos = umbral_fallos
        self.tiempo_espera = tiempo_espera
        self.ultimo_fallo = None
        self.estado = 'CERRADO'  # CERRADO, ABIERTO, MEDIO_ABIERTO
    
    def ejecutar(self, funcion, *args, **kwargs):
        if self.estado == 'ABIERTO':
            if time.time() - self.ultimo_fallo > self.tiempo_espera:
                self.estado = 'MEDIO_ABIERTO'
            else:
                raise CircuitBreakerAbierto("Servicio temporalmente no disponible")
        
        try:
            resultado = funcion(*args, **kwargs)
            self.registrar_exito()
            return resultado
        except Exception as e:
            self.registrar_fallo()
            raise e
```

---

## Logging y Monitoreo

### Configuración de Logs
```python
import logging
import json
from datetime import datetime

# Configuración estructurada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/errores.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SistemaPrediccion')
```

### Métricas en Tiempo Real
```python
class MetricasSistema:
    def __init__(self):
        self.predicciones_exitosas = 0
        self.predicciones_fallidas = 0
        self.tiempo_respuesta_promedio = 0
        self.errores_por_tipo = {}
    
    def registrar_prediccion_exitosa(self, tiempo_respuesta):
        self.predicciones_exitosas += 1
        self.actualizar_tiempo_promedio(tiempo_respuesta)
    
    def registrar_error(self, tipo_error):
        self.predicciones_fallidas += 1
        self.errores_por_tipo[tipo_error] = self.errores_por_tipo.get(tipo_error, 0) + 1
    
    def obtener_tasa_exito(self):
        total = self.predicciones_exitosas + self.predicciones_fallidas
        return self.predicciones_exitosas / total if total > 0 else 0
```

---

## Códigos de Error

### Errores de Validación (E001-E099)
| Código | Descripción | Acción |
|--------|-------------|--------|
| E001 | Campos faltantes | Completar formulario |
| E002 | Tipo de dato incorrecto | Corregir formato |
| E003 | Valor fuera de rango | Verificar datos |
| E004 | Formato inválido | Revisar entrada |

### Errores de Sistema (E100-E199)
| Código | Descripción | Acción |
|--------|-------------|--------|
| E101 | Modelo no disponible | Contactar soporte |
| E102 | Memoria insuficiente | Reintentar más tarde |
| E103 | Timeout de procesamiento | Reducir carga |
| E104 | Error de base de datos | Verificar conexión |

### Errores de Negocio (E200-E299)
| Código | Descripción | Acción |
|--------|-------------|--------|
| E201 | Cliente en lista negra | Rechazar automáticamente |
| E202 | Datos inconsistentes | Revisión manual |
| E203 | Límite de crédito excedido | Reducir monto |

---

## Procedimientos de Emergencia

### 1. Sistema No Responde
```bash
# Verificar estado del servicio
curl -f http://localhost:5000/health || echo "Servicio caído"

# Reiniciar servicio
systemctl restart prediccion-service

# Verificar logs
tail -f logs/errores.log
```

### 2. Memoria Agotada
```python
def liberar_memoria_emergencia():
    import gc
    
    # Forzar recolección de basura
    gc.collect()
    
    # Limpiar cachés
    limpiar_cache_predicciones()
    
    # Reducir workers
    reducir_workers_concurrentes()
    
    logger.warning("Liberación de memoria de emergencia ejecutada")
```

### 3. Tasa de Error Alta
```python
def activar_modo_seguro():
    # Aumentar validaciones
    configuracion.validacion_estricta = True
    
    # Reducir concurrencia
    configuracion.max_workers = 2
    
    # Activar logging detallado
    logging.getLogger().setLevel(logging.DEBUG)
    
    logger.critical("Modo seguro activado debido a alta tasa de errores")
```

### 4. Contactos de Emergencia
- **Soporte Técnico**: soporte@ahorrovalle.com
- **Administrador Sistema**: admin@ahorrovalle.com
- **Teléfono Emergencias**: +57 300 123 4567

---

## Monitoreo y Alertas

### Dashboard de Salud
```python
def obtener_estado_sistema():
    return {
        'timestamp': datetime.now().isoformat(),
        'estado': 'saludable' if obtener_tasa_exito() > 0.95 else 'degradado',
        'metricas': {
            'predicciones_exitosas': metricas.predicciones_exitosas,
            'tasa_exito': f"{obtener_tasa_exito():.2%}",
            'tiempo_respuesta_promedio': f"{metricas.tiempo_respuesta_promedio:.2f}s",
            'memoria_utilizada': f"{obtener_uso_memoria():.1f}%"
        },
        'alertas_activas': obtener_alertas_activas()
    }
```

### Alertas Automáticas
- **Tasa de error > 10%**: Email inmediato
- **Tiempo respuesta > 5s**: Notificación SMS
- **Memoria > 90%**: Alerta crítica
- **Servicio caído**: Llamada automática

---

**Última actualización**: 28 de Octubre, 2025  
**Versión del documento**: 2.0  
**Responsable**: Equipo de Desarrollo Ahorro Valle