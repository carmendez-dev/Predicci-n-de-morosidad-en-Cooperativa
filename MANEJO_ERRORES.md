# 🛡️ MANEJO DE ERRORES Y CASOS EDGE
## Sistema de Predicción de Morosidad - Ahorro Valle

---

## 📋 ÍNDICE

1. [🔍 Tipos de Errores](#-tipos-de-errores)
2. [⚠️ Casos Edge Identificados](#️-casos-edge-identificados)
3. [🛠️ Estrategias de Manejo](#️-estrategias-de-manejo)
4. [📊 Validaciones Implementadas](#-validaciones-implementadas)
5. [🔧 Recuperación de Errores](#-recuperación-de-errores)
6. [📝 Logging y Monitoreo](#-logging-y-monitoreo)
7. [🎯 Casos de Prueba](#-casos-de-prueba)
8. [🚨 Procedimientos de Emergencia](#-procedimientos-de-emergencia)

---

## 🔍 TIPOS DE ERRORES

### 1. **Errores de Entrada de Datos**

#### 1.1 Datos Faltantes
```python
# Ejemplo de manejo
ERROR_CAMPOS_FALTANTES = {
    "error": "validation_error",
    "message": "Campos requeridos faltantes",
    "missing_fields": ["edad", "ingresos_mensuales"],
    "code": "E001"
}
```

**Campos críticos:**
- `edad`: Requerido, rango 18-80
- `ingresos_mensuales`: Requerido, > 0
- `monto_credito`: Requerido, > 0
- `plazo_meses`: Requerido, 1-120

#### 1.2 Tipos de Datos Incorrectos
```python
# Conversiones automáticas implementadas
def convertir_tipos_seguros(datos):
    conversiones = {
        'edad': int,
        'ingresos_mensuales': float,
        'monto_credito': float,
        'plazo_meses': int
    }
    
    for campo, tipo in conversiones.items():
        try:
            if campo in datos:
                datos[campo] = tipo(datos[campo])
        except (ValueError, TypeError):
            return {"error": f"Tipo incorrecto para {campo}"}
    
    return datos
```

#### 1.3 Valores Fuera de Rango
```python
RANGOS_VALIDOS = {
    'edad': (18, 80),
    'ingresos_mensuales': (0, 50000000),  # Hasta 50M COP
    'monto_credito': (100000, 500000000), # 100K - 500M COP
    'plazo_meses': (1, 120),
    'antiguedad_laboral': (0, 50),
    'credito_score': (300, 850),
    'num_pagos_anteriores': (0, 100),
    'num_creditos_anteriores': (0, 50)
}
```

### 2. **Errores del Sistema**

#### 2.1 Modelo No Disponible
```python
def cargar_modelo_con_fallback():
    try:
        # Intentar cargar modelo más reciente
        modelo = cargar_modelo_mas_reciente()
        if modelo is None:
            raise FileNotFoundError("No se encontró modelo")
        return modelo
    except Exception as e:
        logger.error(f"Error cargando modelo: {e}")
        # Fallback a modelo de respaldo
        return cargar_modelo_respaldo()
```

#### 2.2 Errores de Memoria
```python
import psutil
import gc

def verificar_memoria_disponible():
    """Verifica si hay suficiente memoria para la predicción"""
    memoria = psutil.virtual_memory()
    if memoria.percent > 90:
        gc.collect()  # Limpiar memoria
        if memoria.percent > 95:
            raise MemoryError("Memoria insuficiente")
```

#### 2.3 Errores de Disco
```python
import shutil

def verificar_espacio_disco():
    """Verifica espacio en disco para logs"""
    _, _, free = shutil.disk_usage(".")
    if free < 100 * 1024 * 1024:  # Menos de 100MB
        limpiar_logs_antiguos()
```

### 3. **Errores de Red y Conectividad**

```python
from flask import request
import time

def rate_limiting():
    """Limita requests por IP"""
    ip = request.remote_addr
    current_time = time.time()
    
    if ip in request_counts:
        if current_time - request_counts[ip]['last_request'] < 1:
            if request_counts[ip]['count'] > 10:
                return {"error": "Demasiadas solicitudes", "code": "E429"}
```

---

## ⚠️ CASOS EDGE IDENTIFICADOS

### 1. **Datos Extremos**

#### 1.1 Valores Atípicos
```python
VALORES_EXTREMOS = {
    'edad': {
        'min_warning': 18,
        'max_warning': 75,
        'handling': 'Advertencia pero procesar'
    },
    'ingresos_mensuales': {
        'min_warning': 500000,    # Menos de 500K
        'max_warning': 20000000,  # Más de 20M
        'handling': 'Validación adicional'
    },
    'monto_credito': {
        'ratio_ingresos': 10,  # Más de 10x ingresos
        'handling': 'Alerta de alto riesgo'
    }
}
```

#### 1.2 Combinaciones Inusuales
```python
def detectar_combinaciones_inusuales(datos):
    """Detecta patrones atípicos en los datos"""
    alertas = []
    
    # Joven con ingresos muy altos
    if datos['edad'] < 25 and datos['ingresos_mensuales'] > 10000000:
        alertas.append("Ingresos altos para la edad")
    
    # Crédito muy grande vs ingresos
    ratio_credito = datos['monto_credito'] / datos['ingresos_mensuales']
    if ratio_credito > 50:
        alertas.append("Monto desproporcionado a ingresos")
    
    # Muchos créditos anteriores para la edad
    if datos['edad'] < 30 and datos['num_creditos_anteriores'] > 10:
        alertas.append("Historial crediticio extenso para la edad")
    
    return alertas
```

### 2. **Estados del Sistema**

#### 2.1 Primer Uso (Sin Logs)
```python
def inicializar_sistema():
    """Configura el sistema en el primer uso"""
    dirs_necesarios = ['output', 'logs', 'temp', 'backups']
    
    for dir_name in dirs_necesarios:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            logger.info(f"Directorio creado: {dir_name}")
    
    # Verificar modelo
    if not verificar_modelo_existe():
        logger.warning("No se encontró modelo. Ejecutar entrenamiento.")
        return {"warning": "Sistema requiere entrenamiento inicial"}
```

#### 2.2 Múltiples Usuarios Simultáneos
```python
import threading
from queue import Queue

class PredictionQueue:
    def __init__(self, max_concurrent=5):
        self.queue = Queue(maxsize=50)
        self.semaphore = threading.Semaphore(max_concurrent)
        self.processing = {}
    
    def procesar_prediccion(self, datos, request_id):
        try:
            self.semaphore.acquire()
            self.processing[request_id] = time.time()
            resultado = realizar_prediccion(datos)
            return resultado
        finally:
            self.semaphore.release()
            del self.processing[request_id]
```

### 3. **Degradación del Modelo**

#### 3.1 Detección de Drift
```python
def detectar_drift_datos(nuevos_datos):
    """Detecta cambios en la distribución de datos"""
    if len(predicciones_historicas) < 100:
        return False
    
    # Comparar distribuciones
    datos_historicos = obtener_datos_historicos()
    
    # Test KS para variables numéricas
    from scipy.stats import ks_2samp
    
    variables_numericas = ['edad', 'ingresos_mensuales', 'monto_credito']
    drift_detectado = False
    
    for var in variables_numericas:
        hist = [d[var] for d in datos_historicos[-1000:]]
        nuevos = [nuevos_datos[var]]
        
        if len(hist) > 50:
            stat, p_value = ks_2samp(hist, nuevos)
            if p_value < 0.01:
                logger.warning(f"Drift detectado en {var}")
                drift_detectado = True
    
    return drift_detectado
```

#### 3.2 Performance Degradation
```python
def monitorear_performance():
    """Monitorea la performance del modelo"""
    predicciones_recientes = obtener_predicciones_recientes(dias=7)
    
    if len(predicciones_recientes) < 10:
        return {"status": "insufficient_data"}
    
    # Calcular métricas de confianza
    confianzas = [p['probabilidad_max'] for p in predicciones_recientes]
    confianza_promedio = sum(confianzas) / len(confianzas)
    
    if confianza_promedio < 0.6:
        logger.warning("Confianza del modelo por debajo del umbral")
        return {"status": "performance_degraded", "avg_confidence": confianza_promedio}
    
    return {"status": "ok", "avg_confidence": confianza_promedio}
```

---

## 🛠️ ESTRATEGIAS DE MANEJO

### 1. **Validación por Capas**

```python
class ValidadorCapas:
    def __init__(self):
        self.validadores = [
            self.validar_presencia_campos,
            self.validar_tipos_datos,
            self.validar_rangos,
            self.validar_logica_negocio,
            self.validar_coherencia,
            self.validar_seguridad
        ]
    
    def validar_completo(self, datos):
        errores = []
        advertencias = []
        
        for validador in self.validadores:
            try:
                resultado = validador(datos)
                if resultado.get('errores'):
                    errores.extend(resultado['errores'])
                if resultado.get('advertencias'):
                    advertencias.extend(resultado['advertencias'])
            except Exception as e:
                errores.append(f"Error en validación: {str(e)}")
        
        return {
            'valido': len(errores) == 0,
            'errores': errores,
            'advertencias': advertencias
        }
```

### 2. **Circuit Breaker Pattern**

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise e
    
    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'
    
    def reset(self):
        self.failure_count = 0
        self.state = 'CLOSED'
```

### 3. **Graceful Degradation**

```python
def predecir_con_degradacion(datos):
    """Predicción con degradación elegante"""
    try:
        # Intentar predicción completa
        return prediccion_completa(datos)
    
    except ModeloNoDisponibleError:
        # Usar modelo simple/heurístico
        return prediccion_heuristica(datos)
    
    except MemoryError:
        # Predicción con menos features
        return prediccion_reducida(datos)
    
    except Exception as e:
        # Última opción: clasificación básica
        logger.error(f"Error crítico: {e}")
        return clasificacion_basica(datos)

def prediccion_heuristica(datos):
    """Predicción basada en reglas simples"""
    score = 0
    
    # Reglas básicas
    if datos['credito_score'] > 700:
        score += 30
    elif datos['credito_score'] > 600:
        score += 15
    
    ratio_credito = datos['monto_credito'] / datos['ingresos_mensuales']
    if ratio_credito < 5:
        score += 25
    elif ratio_credito < 10:
        score += 10
    
    if datos['antiguedad_laboral'] > 2:
        score += 20
    
    probabilidad_no_moroso = min(score / 100, 0.95)
    
    return {
        'prediccion': 1 if probabilidad_no_moroso > 0.5 else 0,
        'probabilidades': [1 - probabilidad_no_moroso, probabilidad_no_moroso],
        'metodo': 'heuristico',
        'confianza': 'baja'
    }
```

---

## 📊 VALIDACIONES IMPLEMENTADAS

### 1. **Validación Frontend (JavaScript)**

```javascript
class ValidadorFrontend {
    static validarFormulario(datos) {
        const errores = [];
        
        // Validaciones básicas
        if (!datos.edad || datos.edad < 18 || datos.edad > 80) {
            errores.push('Edad debe estar entre 18 y 80 años');
        }
        
        if (!datos.ingresos_mensuales || datos.ingresos_mensuales <= 0) {
            errores.push('Ingresos mensuales deben ser mayor a 0');
        }
        
        if (!datos.monto_credito || datos.monto_credito <= 0) {
            errores.push('Monto del crédito debe ser mayor a 0');
        }
        
        // Validaciones de lógica de negocio
        const ratioCredito = datos.monto_credito / datos.ingresos_mensuales;
        if (ratioCredito > 20) {
            errores.push('El monto solicitado es muy alto comparado con los ingresos');
        }
        
        return {
            valido: errores.length === 0,
            errores: errores
        };
    }
    
    static validarEnTiempoReal(campo, valor) {
        const reglas = {
            edad: {
                pattern: /^\d+$/,
                min: 18,
                max: 80,
                mensaje: 'Edad entre 18 y 80 años'
            },
            ingresos_mensuales: {
                pattern: /^\d+(\.\d{1,2})?$/,
                min: 1,
                mensaje: 'Ingresos deben ser un número positivo'
            }
        };
        
        const regla = reglas[campo];
        if (!regla) return { valido: true };
        
        if (!regla.pattern.test(valor)) {
            return { valido: false, mensaje: regla.mensaje };
        }
        
        const numValor = parseFloat(valor);
        if (regla.min && numValor < regla.min) {
            return { valido: false, mensaje: regla.mensaje };
        }
        
        if (regla.max && numValor > regla.max) {
            return { valido: false, mensaje: regla.mensaje };
        }
        
        return { valido: true };
    }
}
```

### 2. **Validación Backend (Python)**

```python
class ValidadorBackend:
    CAMPOS_REQUERIDOS = [
        'edad', 'genero', 'zona_residencia', 'tipo_empleo',
        'antiguedad_laboral', 'ingresos_mensuales', 'monto_credito',
        'plazo_meses', 'destino_credito'
    ]
    
    TIPOS_ESPERADOS = {
        'edad': int,
        'antiguedad_laboral': int,
        'ingresos_mensuales': float,
        'monto_credito': float,
        'plazo_meses': int,
        'credito_score': int,
        'num_pagos_anteriores': int,
        'num_creditos_anteriores': int
    }
    
    @staticmethod
    def validar_datos(datos):
        errores = []
        advertencias = []
        
        # Verificar campos requeridos
        for campo in ValidadorBackend.CAMPOS_REQUERIDOS:
            if campo not in datos or datos[campo] is None or datos[campo] == '':
                errores.append(f"Campo requerido: {campo}")
        
        # Verificar tipos de datos
        for campo, tipo_esperado in ValidadorBackend.TIPOS_ESPERADOS.items():
            if campo in datos:
                try:
                    datos[campo] = tipo_esperado(datos[campo])
                except (ValueError, TypeError):
                    errores.append(f"Tipo incorrecto para {campo}: esperado {tipo_esperado.__name__}")
        
        # Validaciones de rango
        if 'edad' in datos:
            if not (18 <= datos['edad'] <= 80):
                errores.append("Edad debe estar entre 18 y 80 años")
        
        if 'ingresos_mensuales' in datos:
            if datos['ingresos_mensuales'] <= 0:
                errores.append("Ingresos mensuales deben ser positivos")
            elif datos['ingresos_mensuales'] > 50000000:
                advertencias.append("Ingresos muy altos, verificar datos")
        
        # Validaciones de lógica de negocio
        if 'monto_credito' in datos and 'ingresos_mensuales' in datos:
            ratio = datos['monto_credito'] / datos['ingresos_mensuales']
            if ratio > 30:
                errores.append("Monto del crédito excesivo comparado con ingresos")
            elif ratio > 15:
                advertencias.append("Monto del crédito alto comparado con ingresos")
        
        return {
            'valido': len(errores) == 0,
            'errores': errores,
            'advertencias': advertencias,
            'datos_procesados': datos
        }
```

### 3. **Validación del Modelo**

```python
class ValidadorModelo:
    def __init__(self, modelo, preprocessor):
        self.modelo = modelo
        self.preprocessor = preprocessor
        self.features_esperadas = self._obtener_features_esperadas()
    
    def validar_entrada(self, datos_df):
        """Valida que los datos sean compatibles con el modelo"""
        errores = []
        
        # Verificar shape
        if datos_df.shape[0] == 0:
            errores.append("DataFrame vacío")
            return errores
        
        # Verificar columnas requeridas
        columnas_faltantes = set(self.features_esperadas) - set(datos_df.columns)
        if columnas_faltantes:
            errores.append(f"Columnas faltantes: {list(columnas_faltantes)}")
        
        # Verificar tipos de datos
        for col in datos_df.columns:
            if col in self.features_esperadas:
                if datos_df[col].dtype == 'object':
                    # Verificar valores categóricos válidos
                    if col in self._get_categorical_columns():
                        valores_validos = self._get_valid_categories(col)
                        valores_invalidos = set(datos_df[col].unique()) - set(valores_validos)
                        if valores_invalidos:
                            errores.append(f"Valores inválidos en {col}: {valores_invalidos}")
        
        # Verificar NaN excesivos
        for col in datos_df.columns:
            porcentaje_nan = datos_df[col].isnull().sum() / len(datos_df)
            if porcentaje_nan > 0.8:
                errores.append(f"Demasiados valores faltantes en {col}: {porcentaje_nan:.1%}")
        
        return errores
    
    def predecir_seguro(self, datos_df):
        """Predicción con validaciones adicionales"""
        # Validar entrada
        errores = self.validar_entrada(datos_df)
        if errores:
            raise ValueError(f"Errores de validación: {'; '.join(errores)}")
        
        try:
            # Preprocesar datos
            datos_procesados = self.preprocessor.transform(datos_df)
            
            # Verificar shape después de preprocesamiento
            if datos_procesados.shape[1] != self.modelo.n_features_in_:
                raise ValueError(f"Shape incorrecto después de preprocesamiento: "
                               f"esperado {self.modelo.n_features_in_}, "
                               f"obtenido {datos_procesados.shape[1]}")
            
            # Realizar predicción
            prediccion = self.modelo.predict(datos_procesados)
            probabilidades = self.modelo.predict_proba(datos_procesados)
            
            # Validar resultado
            if not isinstance(prediccion, np.ndarray):
                raise ValueError("Predicción no es un array válido")
            
            if not isinstance(probabilidades, np.ndarray):
                raise ValueError("Probabilidades no son un array válido")
            
            # Verificar rangos de probabilidades
            if not np.all((probabilidades >= 0) & (probabilidades <= 1)):
                raise ValueError("Probabilidades fuera del rango [0,1]")
            
            return prediccion, probabilidades
            
        except Exception as e:
            logger.error(f"Error en predicción segura: {e}")
            raise
```

---

## 🔧 RECUPERACIÓN DE ERRORES

### 1. **Auto-Recuperación del Sistema**

```python
class SistemaAutoRecuperacion:
    def __init__(self):
        self.intentos_maximos = 3
        self.tiempo_espera = [1, 2, 5]  # Backoff exponencial
        self.servicios_criticos = ['modelo', 'preprocessor', 'logger']
    
    def ejecutar_con_reintentos(self, funcion, *args, **kwargs):
        """Ejecuta función con reintentos automáticos"""
        for intento in range(self.intentos_maximos):
            try:
                return funcion(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Intento {intento + 1} falló: {e}")
                
                if intento < self.intentos_maximos - 1:
                    time.sleep(self.tiempo_espera[intento])
                    # Intentar recuperación específica
                    self.intentar_recuperacion(e)
                else:
                    logger.error(f"Todos los intentos fallaron para {funcion.__name__}")
                    raise
    
    def intentar_recuperacion(self, error):
        """Intenta recuperación específica según el tipo de error"""
        error_type = type(error).__name__
        
        if error_type == 'FileNotFoundError':
            self.recuperar_archivos_faltantes()
        elif error_type == 'MemoryError':
            self.liberar_memoria()
        elif error_type == 'ConnectionError':
            self.verificar_conectividad()
        else:
            self.recuperacion_generica()
    
    def recuperar_archivos_faltantes(self):
        """Recupera archivos críticos faltantes"""
        archivos_criticos = [
            'output/model_pipeline_final_*.joblib',
            'logs/sistema.log'
        ]
        
        for patron in archivos_criticos:
            archivos = glob.glob(patron)
            if not archivos:
                logger.warning(f"Archivo faltante: {patron}")
                self.crear_archivo_respaldo(patron)
    
    def liberar_memoria(self):
        """Libera memoria del sistema"""
        import gc
        gc.collect()
        
        # Limpiar cache si existe
        if hasattr(self, 'cache'):
            self.cache.clear()
        
        logger.info("Memoria liberada")
    
    def verificar_conectividad(self):
        """Verifica y restaura conectividad"""
        # Reiniciar conexiones si es necesario
        logger.info("Verificando conectividad del sistema")
```

### 2. **Rollback de Transacciones**

```python
class TransactionManager:
    def __init__(self):
        self.transacciones_activas = {}
        self.snapshots = {}
    
    def iniciar_transaccion(self, transaccion_id):
        """Inicia una nueva transacción"""
        self.transacciones_activas[transaccion_id] = {
            'timestamp': time.time(),
            'operaciones': [],
            'estado': 'activa'
        }
        
        # Crear snapshot del estado actual
        self.snapshots[transaccion_id] = self.crear_snapshot()
    
    def ejecutar_operacion(self, transaccion_id, operacion, *args, **kwargs):
        """Ejecuta operación dentro de transacción"""
        if transaccion_id not in self.transacciones_activas:
            raise ValueError("Transacción no encontrada")
        
        try:
            resultado = operacion(*args, **kwargs)
            self.transacciones_activas[transaccion_id]['operaciones'].append({
                'operacion': operacion.__name__,
                'args': args,
                'kwargs': kwargs,
                'resultado': resultado,
                'timestamp': time.time()
            })
            return resultado
        except Exception as e:
            logger.error(f"Error en operación {operacion.__name__}: {e}")
            self.rollback(transaccion_id)
            raise
    
    def commit(self, transaccion_id):
        """Confirma la transacción"""
        if transaccion_id in self.transacciones_activas:
            self.transacciones_activas[transaccion_id]['estado'] = 'confirmada'
            # Limpiar snapshot
            if transaccion_id in self.snapshots:
                del self.snapshots[transaccion_id]
            logger.info(f"Transacción {transaccion_id} confirmada")
    
    def rollback(self, transaccion_id):
        """Revierte la transacción"""
        if transaccion_id in self.snapshots:
            self.restaurar_snapshot(self.snapshots[transaccion_id])
            del self.snapshots[transaccion_id]
        
        if transaccion_id in self.transacciones_activas:
            self.transacciones_activas[transaccion_id]['estado'] = 'revertida'
            logger.warning(f"Transacción {transaccion_id} revertida")
```

---

## 📝 LOGGING Y MONITOREO

### 1. **Sistema de Logging Estructurado**

```python
import logging
import json
from datetime import datetime

class StructuredLogger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        # Handler para archivo con formato JSON
        handler = logging.FileHandler('logs/structured.log')
        handler.setFormatter(self.JSONFormatter())
        self.logger.addHandler(handler)
    
    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                'timestamp': datetime.fromtimestamp(record.created).isoformat(),
                'level': record.levelname,
                'logger': record.name,
                'message': record.getMessage(),
                'module': record.module,
                'function': record.funcName,
                'line': record.lineno
            }
            
            # Agregar datos adicionales si existen
            if hasattr(record, 'extra_data'):
                log_entry.update(record.extra_data)
            
            return json.dumps(log_entry, ensure_ascii=False)
    
    def log_prediction(self, datos_entrada, resultado, tiempo_procesamiento):
        """Log específico para predicciones"""
        extra_data = {
            'event_type': 'prediction',
            'processing_time_ms': tiempo_procesamiento * 1000,
            'input_features': len(datos_entrada),
            'prediction': resultado.get('prediccion'),
            'confidence': resultado.get('probabilidades', [None, None])[1],
            'risk_level': resultado.get('clasificacion_riesgo')
        }
        
        self.logger.info("Predicción realizada", extra={'extra_data': extra_data})
    
    def log_error(self, error, context=None):
        """Log específico para errores"""
        extra_data = {
            'event_type': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context or {}
        }
        
        self.logger.error("Error en el sistema", extra={'extra_data': extra_data})
```

### 2. **Métricas de Sistema en Tiempo Real**

```python
class SystemMetrics:
    def __init__(self):
        self.metricas = {
            'predicciones_totales': 0,
            'predicciones_exitosas': 0,
            'errores_totales': 0,
            'tiempo_respuesta_promedio': 0,
            'memoria_utilizada': 0,
            'cpu_utilizado': 0,
            'ultima_actualizacion': None
        }
        self.historial = []
    
    def actualizar_metricas(self):
        """Actualiza métricas del sistema"""
        import psutil
        
        self.metricas.update({
            'memoria_utilizada': psutil.virtual_memory().percent,
            'cpu_utilizado': psutil.cpu_percent(),
            'ultima_actualizacion': datetime.now().isoformat()
        })
        
        # Agregar al historial
        self.historial.append(self.metricas.copy())
        
        # Mantener solo últimas 1000 entradas
        if len(self.historial) > 1000:
            self.historial = self.historial[-1000:]
    
    def obtener_estado_salud(self):
        """Obtiene estado de salud del sistema"""
        self.actualizar_metricas()
        
        estado = "saludable"
        alertas = []
        
        if self.metricas['memoria_utilizada'] > 85:
            estado = "advertencia"
            alertas.append("Memoria alta")
        
        if self.metricas['cpu_utilizado'] > 80:
            estado = "advertencia"
            alertas.append("CPU alta")
        
        error_rate = (self.metricas['errores_totales'] / 
                     max(self.metricas['predicciones_totales'], 1))
        
        if error_rate > 0.1:
            estado = "crítico"
            alertas.append(f"Tasa de error alta: {error_rate:.1%}")
        
        return {
            'estado': estado,
            'alertas': alertas,
            'metricas': self.metricas
        }
```

---

## 🎯 CASOS DE PRUEBA

### 1. **Tests de Casos Edge**

```python
import unittest
import pandas as pd

class TestCasosEdge(unittest.TestCase):
    def setUp(self):
        self.predictor = cargar_sistema_prediccion()
    
    def test_datos_extremos_validos(self):
        """Test con datos en los límites válidos"""
        datos_extremos = {
            'edad': 18,
            'genero': 'Femenino',
            'zona_residencia': 'Rural',
            'tipo_empleo': 'Independiente',
            'antiguedad_laboral': 0,
            'ingresos_mensuales': 1000000,  # Mínimo real
            'monto_credito': 100000,        # Mínimo
            'plazo_meses': 1,               # Mínimo
            'destino_credito': 'Personal',
            'tipo_garantia': 'Sin garantía',
            'valor_garantia': 0,
            'credito_score': 300,           # Mínimo
            'num_pagos_anteriores': 0,
            'num_creditos_anteriores': 0,
            'precio_soya': 1000,
            'precio_vino': 5000,
            'uso_productos_financieros': 0
        }
        
        resultado = self.predictor.predecir(datos_extremos)
        self.assertIsNotNone(resultado)
        self.assertIn('prediccion', resultado)
        self.assertIn('probabilidades', resultado)
    
    def test_datos_nulos_parciales(self):
        """Test con algunos campos nulos (no críticos)"""
        datos_con_nulos = {
            'edad': 30,
            'genero': 'Masculino',
            'zona_residencia': 'Urbana',
            'tipo_empleo': 'Empleado',
            'antiguedad_laboral': 5,
            'ingresos_mensuales': 3000000,
            'monto_credito': 10000000,
            'plazo_meses': 12,
            'destino_credito': 'Vivienda',
            'tipo_garantia': None,          # Campo nullable
            'valor_garantia': None,         # Campo nullable
            'credito_score': 650,
            'num_pagos_anteriores': None,   # Se puede imputar
            'num_creditos_anteriores': None, # Se puede imputar
            'precio_soya': 1500,
            'precio_vino': 8000,
            'uso_productos_financieros': 1
        }
        
        resultado = self.predictor.predecir(datos_con_nulos)
        self.assertIsNotNone(resultado)
    
    def test_combinaciones_inusuales(self):
        """Test con combinaciones atípicas pero válidas"""
        casos_inusuales = [
            # Joven con ingresos muy altos
            {
                'edad': 22,
                'ingresos_mensuales': 15000000,
                'monto_credito': 50000000,
                'credito_score': 800
            },
            # Persona mayor con primer crédito
            {
                'edad': 65,
                'ingresos_mensuales': 2000000,
                'monto_credito': 5000000,
                'num_creditos_anteriores': 0,
                'credito_score': 750
            },
            # Crédito muy pequeño con ingresos altos
            {
                'edad': 40,
                'ingresos_mensuales': 10000000,
                'monto_credito': 500000,
                'credito_score': 700
            }
        ]
        
        for caso in casos_inusuales:
            # Completar datos faltantes con valores por defecto
            datos_completos = self.completar_datos_prueba(caso)
            
            resultado = self.predictor.predecir(datos_completos)
            self.assertIsNotNone(resultado)
            # Puede tener advertencias pero debe funcionar
            if 'advertencias' in resultado:
                self.assertIsInstance(resultado['advertencias'], list)
    
    def test_carga_sistema_simultanea(self):
        """Test de múltiples requests simultáneos"""
        import threading
        import time
        
        resultados = []
        errores = []
        
        def realizar_prediccion(thread_id):
            try:
                datos = self.generar_datos_aleatorios()
                inicio = time.time()
                resultado = self.predictor.predecir(datos)
                tiempo = time.time() - inicio
                
                resultados.append({
                    'thread_id': thread_id,
                    'tiempo': tiempo,
                    'exito': True
                })
            except Exception as e:
                errores.append({
                    'thread_id': thread_id,
                    'error': str(e)
                })
        
        # Crear 10 threads simulando usuarios concurrentes
        threads = []
        for i in range(10):
            thread = threading.Thread(target=realizar_prediccion, args=(i,))
            threads.append(thread)
        
        # Iniciar todos los threads
        for thread in threads:
            thread.start()
        
        # Esperar que terminen
        for thread in threads:
            thread.join()
        
        # Verificar resultados
        self.assertGreater(len(resultados), 0, "Debería haber al menos un resultado exitoso")
        self.assertLess(len(errores), 5, "No debería haber muchos errores concurrentes")
        
        # Verificar tiempos de respuesta
        tiempos = [r['tiempo'] for r in resultados]
        tiempo_promedio = sum(tiempos) / len(tiempos)
        self.assertLess(tiempo_promedio, 5.0, "Tiempo de respuesta muy alto bajo carga")
    
    def completar_datos_prueba(self, datos_parciales):
        """Completa datos para pruebas"""
        datos_base = {
            'edad': 35,
            'genero': 'Masculino',
            'zona_residencia': 'Urbana',
            'tipo_empleo': 'Empleado',
            'antiguedad_laboral': 3,
            'ingresos_mensuales': 3000000,
            'monto_credito': 10000000,
            'plazo_meses': 24,
            'destino_credito': 'Personal',
            'tipo_garantia': 'Hipotecaria',
            'valor_garantia': 15000000,
            'credito_score': 650,
            'num_pagos_anteriores': 5,
            'num_creditos_anteriores': 2,
            'precio_soya': 1500,
            'precio_vino': 8000,
            'uso_productos_financieros': 1
        }
        
        datos_base.update(datos_parciales)
        return datos_base
    
    def generar_datos_aleatorios(self):
        """Genera datos aleatorios válidos para pruebas"""
        import random
        
        return {
            'edad': random.randint(18, 70),
            'genero': random.choice(['Masculino', 'Femenino']),
            'zona_residencia': random.choice(['Urbana', 'Rural']),
            'tipo_empleo': random.choice(['Empleado', 'Independiente']),
            'antiguedad_laboral': random.randint(0, 20),
            'ingresos_mensuales': random.randint(1000000, 8000000),
            'monto_credito': random.randint(1000000, 50000000),
            'plazo_meses': random.randint(6, 60),
            'destino_credito': random.choice(['Personal', 'Vivienda', 'Vehiculo']),
            'tipo_garantia': random.choice(['Hipotecaria', 'Prendaria', 'Sin garantía']),
            'valor_garantia': random.randint(0, 100000000),
            'credito_score': random.randint(300, 850),
            'num_pagos_anteriores': random.randint(0, 20),
            'num_creditos_anteriores': random.randint(0, 10),
            'precio_soya': random.randint(1000, 2000),
            'precio_vino': random.randint(5000, 12000),
            'uso_productos_financieros': random.randint(0, 5)
        }

if __name__ == '__main__':
    unittest.main()
```

### 2. **Tests de Performance**

```python
class TestPerformance(unittest.TestCase):
    def test_tiempo_respuesta_individual(self):
        """Test de tiempo de respuesta para predicción individual"""
        datos = self.generar_datos_prueba()
        
        inicio = time.time()
        resultado = self.predictor.predecir(datos)
        tiempo_total = time.time() - inicio
        
        self.assertLess(tiempo_total, 2.0, "Predicción individual muy lenta")
        self.assertIsNotNone(resultado)
    
    def test_throughput_sistema(self):
        """Test de throughput del sistema"""
        datos_prueba = [self.generar_datos_prueba() for _ in range(100)]
        
        inicio = time.time()
        resultados_exitosos = 0
        
        for datos in datos_prueba:
            try:
                resultado = self.predictor.predecir(datos)
                if resultado:
                    resultados_exitosos += 1
            except Exception:
                pass
        
        tiempo_total = time.time() - inicio
        throughput = resultados_exitosos / tiempo_total
        
        self.assertGreater(throughput, 10, "Throughput muy bajo")
        self.assertGreater(resultados_exitosos, 95, "Muchas predicciones fallaron")
    
    def test_uso_memoria(self):
        """Test de uso de memoria durante operación"""
        import psutil
        import gc
        
        # Limpiar memoria antes de test
        gc.collect()
        memoria_inicial = psutil.virtual_memory().percent
        
        # Realizar múltiples predicciones
        for _ in range(50):
            datos = self.generar_datos_prueba()
            self.predictor.predecir(datos)
        
        memoria_final = psutil.virtual_memory().percent
        incremento_memoria = memoria_final - memoria_inicial
        
        self.assertLess(incremento_memoria, 10, "Incremento de memoria excesivo")
```

---

## 🚨 PROCEDIMIENTOS DE EMERGENCIA

### 1. **Plan de Contingencia**

```python
class PlanContingencia:
    def __init__(self):
        self.estado_sistema = "normal"
        self.procedimientos_emergencia = {
            'modelo_no_disponible': self.emergencia_modelo,
            'memoria_agotada': self.emergencia_memoria,
            'errores_masivos': self.emergencia_errores,
            'carga_excesiva': self.emergencia_carga
        }
    
    def detectar_emergencia(self):
        """Detecta situaciones de emergencia"""
        # Verificar modelo
        if not self.verificar_modelo_disponible():
            return 'modelo_no_disponible'
        
        # Verificar memoria
        if psutil.virtual_memory().percent > 95:
            return 'memoria_agotada'
        
        # Verificar tasa de errores
        if self.obtener_tasa_errores() > 0.5:
            return 'errores_masivos'
        
        # Verificar carga del sistema
        if self.obtener_requests_por_minuto() > 1000:
            return 'carga_excesiva'
        
        return None
    
    def ejecutar_contingencia(self):
        """Ejecuta plan de contingencia apropiado"""
        emergencia = self.detectar_emergencia()
        
        if emergencia:
            logger.critical(f"EMERGENCIA DETECTADA: {emergencia}")
            self.estado_sistema = "emergencia"
            
            procedimiento = self.procedimientos_emergencia.get(emergencia)
            if procedimiento:
                procedimiento()
            
            self.notificar_administrador(emergencia)
    
    def emergencia_modelo(self):
        """Procedimiento para modelo no disponible"""
        logger.critical("EMERGENCIA: Modelo no disponible")
        
        # 1. Intentar recargar modelo
        try:
            self.recargar_modelo()
            logger.info("Modelo recargado exitosamente")
            return
        except Exception as e:
            logger.error(f"No se pudo recargar modelo: {e}")
        
        # 2. Usar modelo de respaldo
        try:
            self.cargar_modelo_respaldo()
            logger.warning("Usando modelo de respaldo")
            return
        except Exception as e:
            logger.error(f"No se pudo cargar modelo de respaldo: {e}")
        
        # 3. Activar modo de solo lectura
        self.activar_modo_solo_lectura()
        logger.critical("Sistema en modo solo lectura")
    
    def emergencia_memoria(self):
        """Procedimiento para memoria agotada"""
        logger.critical("EMERGENCIA: Memoria agotada")
        
        # 1. Forzar liberación de memoria
        import gc
        gc.collect()
        
        # 2. Limpiar caches
        self.limpiar_caches()
        
        # 3. Reducir capacidad del sistema
        self.reducir_capacidad_concurrente()
        
        # 4. Si persiste, reiniciar sistema
        if psutil.virtual_memory().percent > 90:
            self.programar_reinicio()
    
    def emergencia_errores(self):
        """Procedimiento para errores masivos"""
        logger.critical("EMERGENCIA: Errores masivos detectados")
        
        # 1. Activar circuit breaker
        self.activar_circuit_breaker()
        
        # 2. Cambiar a validaciones mínimas
        self.activar_modo_validacion_minima()
        
        # 3. Guardar logs de emergencia
        self.crear_dump_emergencia()
    
    def emergencia_carga(self):
        """Procedimiento para carga excesiva"""
        logger.critical("EMERGENCIA: Carga excesiva")
        
        # 1. Activar rate limiting agresivo
        self.activar_rate_limiting_agresivo()
        
        # 2. Rechazar requests no críticos
        self.activar_modo_solo_criticos()
        
        # 3. Enviar respuestas de "sistema ocupado"
        self.activar_respuestas_ocupado()
    
    def notificar_administrador(self, tipo_emergencia):
        """Notifica al administrador sobre la emergencia"""
        mensaje = {
            'timestamp': datetime.now().isoformat(),
            'tipo': tipo_emergencia,
            'estado_sistema': self.estado_sistema,
            'metricas': self.obtener_metricas_criticas()
        }
        
        # Guardar notificación
        with open('logs/emergencias.json', 'a') as f:
            json.dump(mensaje, f, ensure_ascii=False)
            f.write('\n')
        
        logger.critical(f"NOTIFICACIÓN ADMINISTRADOR: {mensaje}")
```

### 2. **Procedimientos de Recuperación**

```python
class ProcedimientosRecuperacion:
    def recuperacion_completa(self):
        """Procedimiento de recuperación completa del sistema"""
        logger.info("Iniciando recuperación completa del sistema")
        
        pasos_recuperacion = [
            ('Verificar integridad de archivos', self.verificar_integridad),
            ('Reconstruir modelo si necesario', self.reconstruir_modelo),
            ('Verificar conectividad', self.verificar_conectividad),
            ('Restaurar configuración', self.restaurar_configuracion),
            ('Validar funcionamiento', self.validar_funcionamiento),
            ('Restaurar servicio completo', self.restaurar_servicio)
        ]
        
        for descripcion, funcion in pasos_recuperacion:
            try:
                logger.info(f"Ejecutando: {descripcion}")
                resultado = funcion()
                if not resultado:
                    logger.error(f"Falló: {descripcion}")
                    return False
                logger.info(f"Completado: {descripcion}")
            except Exception as e:
                logger.error(f"Error en {descripcion}: {e}")
                return False
        
        logger.info("Recuperación completa exitosa")
        return True
    
    def recuperacion_rapida(self):
        """Recuperación rápida para problemas menores"""
        logger.info("Iniciando recuperación rápida")
        
        try:
            # Limpiar recursos
            self.limpiar_recursos()
            
            # Recargar componentes críticos
            self.recargar_componentes_criticos()
            
            # Verificar funcionamiento básico
            if self.test_funcionamiento_basico():
                logger.info("Recuperación rápida exitosa")
                return True
            else:
                logger.warning("Recuperación rápida falló, requiere recuperación completa")
                return self.recuperacion_completa()
                
        except Exception as e:
            logger.error(f"Error en recuperación rápida: {e}")
            return False
    
    def crear_punto_restauracion(self):
        """Crea un punto de restauración del sistema"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        punto_restauracion = f"backup/restauracion_{timestamp}"
        
        try:
            os.makedirs(punto_restauracion, exist_ok=True)
            
            # Copiar archivos críticos
            archivos_criticos = [
                'output/model_pipeline_final_*.joblib',
                'logs/sistema.log',
                'config/*.json'
            ]
            
            for patron in archivos_criticos:
                archivos = glob.glob(patron)
                for archivo in archivos:
                    destino = os.path.join(punto_restauracion, os.path.basename(archivo))
                    shutil.copy2(archivo, destino)
            
            # Guardar estado del sistema
            estado = {
                'timestamp': timestamp,
                'version_sistema': self.obtener_version_sistema(),
                'configuracion': self.obtener_configuracion_actual(),
                'metricas': self.obtener_metricas_sistema()
            }
            
            with open(os.path.join(punto_restauracion, 'estado_sistema.json'), 'w') as f:
                json.dump(estado, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Punto de restauración creado: {punto_restauracion}")
            return punto_restauracion
            
        except Exception as e:
            logger.error(f"Error creando punto de restauración: {e}")
            return None
```

---

## 📊 DASHBOARD DE MONITOREO

```python
class DashboardMonitoreo:
    def __init__(self):
        self.metricas_tiempo_real = {}
        self.alertas_activas = []
        self.estado_componentes = {}
    
    def generar_reporte_salud(self):
        """Genera reporte completo de salud del sistema"""
        return {
            'timestamp': datetime.now().isoformat(),
            'estado_general': self.calcular_estado_general(),
            'componentes': {
                'modelo': self.verificar_estado_modelo(),
                'base_datos': self.verificar_estado_bd(),
                'memoria': self.verificar_estado_memoria(),
                'disco': self.verificar_estado_disco(),
                'red': self.verificar_estado_red()
            },
            'metricas_performance': {
                'predicciones_por_minuto': self.calcular_ppm(),
                'tiempo_respuesta_promedio': self.calcular_tiempo_respuesta(),
                'tasa_exito': self.calcular_tasa_exito(),
                'tasa_error': self.calcular_tasa_error()
            },
            'alertas': self.alertas_activas,
            'recomendaciones': self.generar_recomendaciones()
        }
    
    def calcular_estado_general(self):
        """Calcula el estado general del sistema"""
        estados_componentes = [
            self.verificar_estado_modelo(),
            self.verificar_estado_memoria(),
            self.verificar_estado_disco()
        ]
        
        if all(estado == 'ok' for estado in estados_componentes):
            return 'saludable'
        elif any(estado == 'critico' for estado in estados_componentes):
            return 'critico'
        else:
            return 'advertencia'
    
    def generar_recomendaciones(self):
        """Genera recomendaciones basadas en el estado actual"""
        recomendaciones = []
        
        if self.calcular_tasa_error() > 0.1:
            recomendaciones.append({
                'tipo': 'critico',
                'mensaje': 'Tasa de error alta - Revisar logs de errores',
                'accion': 'Investigar causas de errores recientes'
            })
        
        memoria_uso = psutil.virtual_memory().percent
        if memoria_uso > 80:
            recomendaciones.append({
                'tipo': 'advertencia',
                'mensaje': f'Uso de memoria alto: {memoria_uso:.1f}%',
                'accion': 'Considerar optimización o aumento de memoria'
            })
        
        return recomendaciones
```

---

**📋 Resumen de Estrategias Implementadas:**

✅ **Validación por Capas**: Frontend → Backend → Modelo
✅ **Circuit Breaker**: Protección contra fallos en cascada  
✅ **Auto-recuperación**: Reintentos automáticos con backoff
✅ **Graceful Degradation**: Funcionalidad reducida vs fallo total
✅ **Logging Estructurado**: Monitoreo y debugging efectivo
✅ **Tests Automatizados**: Validación de casos edge
✅ **Planes de Contingencia**: Procedimientos de emergencia
✅ **Monitoreo en Tiempo Real**: Dashboard de salud del sistema

*Este sistema está diseñado para ser robusto, tolerante a fallos y recuperable ante cualquier situación imprevista.*

**Última actualización:** 27 de Octubre, 2025