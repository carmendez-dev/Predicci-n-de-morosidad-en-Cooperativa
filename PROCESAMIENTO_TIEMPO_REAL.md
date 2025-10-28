# ⚡ PROCESAMIENTO DE DATOS EN TIEMPO REAL
## Sistema de Predicción de Morosidad - Ahorro Valle

---

## 📋 ÍNDICE

1. [🎯 Introducción al Procesamiento en Tiempo Real](#-introducción-al-procesamiento-en-tiempo-real)
2. [🔄 Flujo de Datos Completo](#-flujo-de-datos-completo)
3. [📊 Pipeline de Procesamiento](#-pipeline-de-procesamiento)
4. [🛠️ Componentes del Sistema](#️-componentes-del-sistema)
5. [⚡ Optimizaciones de Performance](#-optimizaciones-de-performance)
6. [📈 Monitoreo en Tiempo Real](#-monitoreo-en-tiempo-real)
7. [🔧 Configuración Avanzada](#-configuración-avanzada)
8. [🚨 Manejo de Errores en Tiempo Real](#-manejo-de-errores-en-tiempo-real)
9. [📊 Métricas y KPIs](#-métricas-y-kpis)

---

## 🎯 INTRODUCCIÓN AL PROCESAMIENTO EN TIEMPO REAL

### ¿Qué es el Procesamiento en Tiempo Real?

El **procesamiento en tiempo real** en nuestro sistema se refiere a la capacidad de:
- ✅ **Recibir datos** del usuario instantáneamente
- ✅ **Validar y procesar** información en < 2 segundos
- ✅ **Ejecutar predicciones** de ML inmediatamente
- ✅ **Devolver resultados** al usuario sin demoras perceptibles
- ✅ **Actualizar métricas** automáticamente

### Características del Sistema en Tiempo Real

```
ENTRADA → VALIDACIÓN → PROCESAMIENTO → PREDICCIÓN → RESPUESTA
   ↓          ↓             ↓            ↓           ↓
 < 0.1s    < 0.2s        < 0.5s       < 1.0s     < 0.3s
   │          │             │            │           │
   └──────────┴─────────────┴────────────┴───────────┘
              TIEMPO TOTAL: < 2.0 segundos
```

### Ventajas del Procesamiento en Tiempo Real

#### 🚀 **Para el Usuario:**
- Respuesta inmediata a solicitudes
- Experiencia fluida e interactiva
- Feedback instantáneo sobre errores
- Validación en tiempo real de formularios

#### 📊 **Para el Negocio:**
- Mayor throughput de evaluaciones
- Decisiones más rápidas
- Mejor experiencia del cliente final
- Eficiencia operacional mejorada

#### 🔧 **Para el Sistema:**
- Uso eficiente de recursos
- Escalabilidad mejorada
- Monitoreo continuo
- Detección temprana de problemas

---

## 🔄 FLUJO DE DATOS COMPLETO

### Arquitectura de Procesamiento

```
    USUARIO (Frontend)
         │
         ▼
┌─────────────────────┐
│   NAVEGADOR WEB     │ ◄─── Validación JavaScript
│                     │      Tiempo Real
└─────────┬───────────┘
          │ HTTP POST /predecir
          ▼
┌─────────────────────┐
│   SERVIDOR FLASK    │
│                     │
│ ┌─────────────────┐ │ ◄─── Recepción Request
│ │  Request        │ │      < 0.1s
│ │  Handler        │ │
│ └─────────────────┘ │
│          │          │
│          ▼          │
│ ┌─────────────────┐ │ ◄─── Validación Backend
│ │  Validador      │ │      < 0.2s
│ │  Backend        │ │
│ └─────────────────┘ │
│          │          │
│          ▼          │
│ ┌─────────────────┐ │ ◄─── Preprocesamiento
│ │  Data           │ │      < 0.3s
│ │  Preprocessor   │ │
│ └─────────────────┘ │
│          │          │
│          ▼          │
│ ┌─────────────────┐ │ ◄─── Predicción ML
│ │  ML Engine      │ │      < 1.0s
│ │  (Modelo)       │ │
│ └─────────────────┘ │
│          │          │
│          ▼          │
│ ┌─────────────────┐ │ ◄─── Post-procesamiento
│ │  Result         │ │      < 0.2s
│ │  Processor      │ │
│ └─────────────────┘ │
│          │          │
│          ▼          │
│ ┌─────────────────┐ │ ◄─── Logging
│ │  Logger &       │ │      < 0.1s
│ │  Metrics        │ │
│ └─────────────────┘ │
└─────────┬───────────┘
          │ JSON Response
          ▼
┌─────────────────────┐
│   NAVEGADOR WEB     │ ◄─── Render Resultado
│   (Actualización)   │      < 0.1s
└─────────────────────┘
          │
          ▼
    USUARIO (Resultado)
```

### Flujo Temporal Detallado

```python
# Timestamps típicos de una predicción
t0 = 0.000s    # Usuario envía formulario
t1 = 0.050s    # Request llega al servidor
t2 = 0.150s    # Validación completada
t3 = 0.400s    # Preprocesamiento terminado
t4 = 1.200s    # Predicción ML completada
t5 = 1.350s    # Post-procesamiento terminado
t6 = 1.400s    # Log guardado
t7 = 1.450s    # Response enviado
t8 = 1.500s    # Usuario ve resultado

TIEMPO TOTAL: 1.5 segundos (promedio)
```

---

## 📊 PIPELINE DE PROCESAMIENTO

### 1. **Recepción de Datos (Frontend → Backend)**

```javascript
// Frontend: Envío de datos en tiempo real
function enviarPrediccion() {
    const timestamp_inicio = performance.now();
    
    // Validación frontend inmediata
    const datosValidados = validarFormulario();
    if (!datosValidados.valido) {
        mostrarErrores(datosValidados.errores);
        return; // < 50ms
    }
    
    // Envío AJAX asíncrono
    fetch('/predecir', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Request-ID': generarRequestID()
        },
        body: JSON.stringify({
            datos: datosFormulario,
            timestamp_cliente: timestamp_inicio,
            session_id: obtenerSessionID()
        })
    })
    .then(response => response.json())
    .then(resultado => {
        const tiempo_total = performance.now() - timestamp_inicio;
        mostrarResultado(resultado, tiempo_total);
    })
    .catch(error => manejarError(error));
}
```

### 2. **Procesamiento Backend en Tiempo Real**

```python
from flask import Flask, request, jsonify
import time
import threading
from queue import Queue
import logging

app = Flask(__name__)

# Cola para procesamiento asíncrono
cola_predicciones = Queue(maxsize=100)
procesador_activo = True

class ProcesadorTiempoReal:
    def __init__(self):
        self.modelo = None
        self.preprocessor = None
        self.cache_modelo = {}
        self.metricas_tiempo_real = {
            'predicciones_por_minuto': 0,
            'tiempo_promedio_respuesta': 0,
            'errores_por_minuto': 0,
            'cache_hits': 0
        }
        self.inicializar_componentes()
        
    def inicializar_componentes(self):
        """Inicialización optimizada de componentes"""
        start_time = time.time()
        
        # Cargar modelo una sola vez al iniciar
        self.modelo, self.preprocessor = self.cargar_modelo_optimizado()
        
        # Pre-calentar modelo con datos dummy
        self.precalentar_modelo()
        
        load_time = time.time() - start_time
        logging.info(f"Componentes inicializados en {load_time:.3f}s")
    
    def precalentar_modelo(self):
        """Pre-calienta el modelo para mejorar primera predicción"""
        datos_dummy = self.generar_datos_dummy()
        
        try:
            # Hacer predicción dummy para cargar modelo en memoria
            _ = self.procesar_prediccion_interna(datos_dummy)
            logging.info("Modelo pre-calentado exitosamente")
        except Exception as e:
            logging.warning(f"Error pre-calentando modelo: {e}")

@app.route('/predecir', methods=['POST'])
def predecir_tiempo_real():
    """Endpoint principal para predicciones en tiempo real"""
    
    # Timestamp de inicio
    timestamp_inicio = time.time()
    request_id = request.headers.get('X-Request-ID', 'unknown')
    
    try:
        # 1. RECEPCIÓN Y VALIDACIÓN RÁPIDA (< 0.1s)
        datos_raw = request.get_json()
        
        if not datos_raw:
            return jsonify({
                'error': 'No se recibieron datos',
                'codigo': 'E001',
                'tiempo_procesamiento': 0
            }), 400
        
        # 2. VALIDACIÓN BACKEND (< 0.2s)
        resultado_validacion = validador.validar_datos_rapido(datos_raw['datos'])
        
        if not resultado_validacion['valido']:
            return jsonify({
                'error': 'Datos inválidos',
                'errores': resultado_validacion['errores'],
                'codigo': 'E002',
                'tiempo_procesamiento': time.time() - timestamp_inicio
            }), 400
        
        # 3. PROCESAMIENTO EN TIEMPO REAL
        resultado = procesador.procesar_prediccion(
            datos=resultado_validacion['datos_procesados'],
            request_id=request_id,
            timestamp_inicio=timestamp_inicio
        )
        
        # 4. RESPUESTA RÁPIDA
        tiempo_total = time.time() - timestamp_inicio
        resultado['tiempo_procesamiento'] = tiempo_total
        resultado['request_id'] = request_id
        
        # Log asíncrono para no bloquear respuesta
        threading.Thread(
            target=logger_asincrono,
            args=(resultado, tiempo_total, request_id)
        ).start()
        
        return jsonify(resultado)
        
    except Exception as e:
        tiempo_error = time.time() - timestamp_inicio
        logging.error(f"Error en predicción {request_id}: {e}")
        
        return jsonify({
            'error': 'Error interno del servidor',
            'codigo': 'E500',
            'tiempo_procesamiento': tiempo_error,
            'request_id': request_id
        }), 500

def logger_asincrono(resultado, tiempo_procesamiento, request_id):
    """Logger asíncrono para no bloquear respuesta"""
    try:
        log_entry = {
            'timestamp': time.time(),
            'request_id': request_id,
            'resultado': resultado,
            'tiempo_procesamiento': tiempo_procesamiento,
            'memoria_usada': obtener_uso_memoria(),
            'cpu_usado': obtener_uso_cpu()
        }
        
        # Guardar en archivo
        guardar_log_prediccion(log_entry)
        
        # Actualizar métricas en tiempo real
        actualizar_metricas_tiempo_real(tiempo_procesamiento)
        
    except Exception as e:
        logging.error(f"Error en logger asíncrono: {e}")
```

### 3. **Preprocesamiento Optimizado**

```python
class PreprocessorTiempoReal:
    def __init__(self):
        self.transformadores_cargados = {}
        self.cache_transformaciones = {}
        self.estadisticas_cache = {'hits': 0, 'misses': 0}
        
    def procesar_datos_optimizado(self, datos):
        """Preprocesamiento optimizado para tiempo real"""
        timestamp_inicio = time.time()
        
        # 1. Crear clave de cache para datos similares
        cache_key = self.generar_cache_key(datos)
        
        # 2. Verificar cache primero
        if cache_key in self.cache_transformaciones:
            self.estadisticas_cache['hits'] += 1
            cached_result = self.cache_transformaciones[cache_key]
            
            logging.debug(f"Cache hit - Procesamiento en {time.time() - timestamp_inicio:.4f}s")
            return cached_result
        
        self.estadisticas_cache['misses'] += 1
        
        # 3. Procesamiento completo si no está en cache
        try:
            # Crear DataFrame optimizado
            df = self.crear_dataframe_optimizado(datos)
            
            # Aplicar transformaciones
            datos_procesados = self.aplicar_transformaciones_rapidas(df)
            
            # Guardar en cache (limitado a últimas 100 transformaciones)
            if len(self.cache_transformaciones) < 100:
                self.cache_transformaciones[cache_key] = datos_procesados
            
            tiempo_procesamiento = time.time() - timestamp_inicio
            logging.debug(f"Procesamiento completo en {tiempo_procesamiento:.4f}s")
            
            return datos_procesados
            
        except Exception as e:
            logging.error(f"Error en preprocesamiento: {e}")
            raise
    
    def crear_dataframe_optimizado(self, datos):
        """Crea DataFrame optimizado para velocidad"""
        # Pre-definir tipos de datos para evitar inferencia
        tipos_datos = {
            'edad': 'int32',
            'ingresos_mensuales': 'float32',
            'monto_credito': 'float32',
            'credito_score': 'int32'
            # ... otros campos
        }
        
        # Crear DataFrame con tipos específicos
        df = pd.DataFrame([datos], dtype='object')
        
        # Convertir tipos eficientemente
        for columna, tipo in tipos_datos.items():
            if columna in df.columns:
                df[columna] = df[columna].astype(tipo)
        
        return df
    
    def aplicar_transformaciones_rapidas(self, df):
        """Aplica transformaciones optimizadas para velocidad"""
        
        # 1. Imputación rápida (valores pre-calculados)
        df = self.imputar_valores_rapido(df)
        
        # 2. Escalado usando transformadores pre-cargados
        df_numerico = self.escalar_numericas_rapido(df)
        
        # 3. Encoding categóricas (mapping pre-definido)
        df_categorico = self.encode_categoricas_rapido(df)
        
        # 4. Combinar resultados
        resultado_final = np.hstack([df_numerico, df_categorico])
        
        return resultado_final
```

### 4. **Predicción ML Optimizada**

```python
class ModeloTiempoReal:
    def __init__(self):
        self.modelo_cargado = None
        self.cache_predicciones = {}
        self.estadisticas_modelo = {
            'predicciones_realizadas': 0,
            'cache_hits_modelo': 0,
            'tiempo_promedio_prediccion': 0
        }
        
    def predecir_optimizado(self, datos_procesados):
        """Predicción optimizada para tiempo real"""
        timestamp_inicio = time.time()
        
        try:
            # 1. Verificar cache de predicciones similares
            cache_key = hash(datos_procesados.tobytes())
            
            if cache_key in self.cache_predicciones:
                self.estadisticas_modelo['cache_hits_modelo'] += 1
                resultado_cache = self.cache_predicciones[cache_key]
                
                logging.debug("Cache hit en predicción ML")
                return resultado_cache
            
            # 2. Predicción real
            prediccion = self.modelo_cargado.predict(datos_procesados)
            probabilidades = self.modelo_cargado.predict_proba(datos_procesados)
            
            # 3. Procesar resultado
            resultado = {
                'prediccion': int(prediccion[0]),
                'probabilidades': probabilidades[0].tolist(),
                'confianza': float(np.max(probabilidades[0]))
            }
            
            # 4. Guardar en cache (últimas 50 predicciones)
            if len(self.cache_predicciones) < 50:
                self.cache_predicciones[cache_key] = resultado
            
            # 5. Actualizar estadísticas
            tiempo_prediccion = time.time() - timestamp_inicio
            self.actualizar_estadisticas_modelo(tiempo_prediccion)
            
            return resultado
            
        except Exception as e:
            logging.error(f"Error en predicción ML: {e}")
            raise
    
    def actualizar_estadisticas_modelo(self, tiempo_prediccion):
        """Actualiza estadísticas del modelo en tiempo real"""
        self.estadisticas_modelo['predicciones_realizadas'] += 1
        
        # Calcular promedio móvil del tiempo de predicción
        n = self.estadisticas_modelo['predicciones_realizadas']
        promedio_anterior = self.estadisticas_modelo['tiempo_promedio_prediccion']
        
        nuevo_promedio = ((promedio_anterior * (n-1)) + tiempo_prediccion) / n
        self.estadisticas_modelo['tiempo_promedio_prediccion'] = nuevo_promedio
```

---

## 🛠️ COMPONENTES DEL SISTEMA

### Arquitectura de Componentes en Tiempo Real

```python
# Singleton para gestión centralizada
class SistemaTiempoReal:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SistemaTiempoReal, cls).__new__(cls)
            cls._instance.inicializado = False
        return cls._instance
    
    def __init__(self):
        if not self.inicializado:
            self.inicializar_sistema()
            self.inicializado = True
    
    def inicializar_sistema(self):
        """Inicialización optimizada del sistema completo"""
        
        # 1. Pool de Workers para procesamiento concurrente
        self.pool_workers = ThreadPoolExecutor(max_workers=4)
        
        # 2. Cache distribuido en memoria
        self.cache_sistema = {
            'modelos': {},
            'transformaciones': {},
            'predicciones': {},
            'estadisticas': {}
        }
        
        # 3. Métricas en tiempo real
        self.metricas_tiempo_real = MetricasTiempoReal()
        
        # 4. Monitor de sistema
        self.monitor_sistema = MonitorSistema()
        
        # 5. Queue para procesamiento asíncrono
        self.cola_procesamiento = Queue(maxsize=1000)
        
        # 6. Iniciar workers background
        self.iniciar_workers_background()
    
    def iniciar_workers_background(self):
        """Inicia workers para procesamiento background"""
        
        # Worker para logging asíncrono
        threading.Thread(
            target=self.worker_logging,
            daemon=True
        ).start()
        
        # Worker para actualización de métricas
        threading.Thread(
            target=self.worker_metricas,
            daemon=True
        ).start()
        
        # Worker para limpieza de cache
        threading.Thread(
            target=self.worker_limpieza_cache,
            daemon=True
        ).start()
```

### Gestión de Memoria y Recursos

```python
class GestorRecursos:
    def __init__(self):
        self.limite_memoria = 1024 * 1024 * 1024  # 1GB
        self.limite_cache_entradas = 1000
        self.intervalo_limpieza = 300  # 5 minutos
        
    def monitorear_recursos(self):
        """Monitorea recursos del sistema continuamente"""
        import psutil
        
        while True:
            # Verificar uso de memoria
            memoria_actual = psutil.virtual_memory()
            
            if memoria_actual.percent > 85:
                self.limpiar_caches_agresivo()
                logging.warning(f"Memoria alta: {memoria_actual.percent}%")
            
            # Verificar uso de CPU
            cpu_actual = psutil.cpu_percent(interval=1)
            
            if cpu_actual > 80:
                self.reducir_workers_temporalmente()
                logging.warning(f"CPU alta: {cpu_actual}%")
            
            time.sleep(30)  # Verificar cada 30 segundos
    
    def limpiar_caches_agresivo(self):
        """Limpieza agresiva de caches cuando memoria es alta"""
        # Limpiar cache de predicciones más antiguas
        self.limpiar_cache_por_timestamp()
        
        # Forzar garbage collection
        import gc
        gc.collect()
        
        logging.info("Limpieza agresiva de cache completada")
```

---

## ⚡ OPTIMIZACIONES DE PERFORMANCE

### 1. **Caching Inteligente**

```python
class CacheInteligente:
    def __init__(self):
        self.cache_l1 = {}  # Cache más rápido (en memoria)
        self.cache_l2 = {}  # Cache secundario
        self.estadisticas_cache = {
            'l1_hits': 0,
            'l2_hits': 0,
            'misses': 0,
            'total_requests': 0
        }
        
    def obtener_prediccion_cache(self, hash_datos):
        """Obtiene predicción del cache multinivel"""
        self.estadisticas_cache['total_requests'] += 1
        
        # Nivel 1 - Cache más rápido
        if hash_datos in self.cache_l1:
            self.estadisticas_cache['l1_hits'] += 1
            return self.cache_l1[hash_datos]
        
        # Nivel 2 - Cache secundario
        if hash_datos in self.cache_l2:
            self.estadisticas_cache['l2_hits'] += 1
            # Promover a L1
            self.cache_l1[hash_datos] = self.cache_l2[hash_datos]
            return self.cache_l2[hash_datos]
        
        # Cache miss
        self.estadisticas_cache['misses'] += 1
        return None
    
    def guardar_en_cache(self, hash_datos, resultado):
        """Guarda resultado en cache multinivel"""
        # Siempre guardar en L1 primero
        self.cache_l1[hash_datos] = resultado
        
        # Gestionar tamaño de cache L1
        if len(self.cache_l1) > 100:
            # Mover elementos más antiguos a L2
            items_antiguos = list(self.cache_l1.items())[:50]
            for key, value in items_antiguos:
                self.cache_l2[key] = value
                del self.cache_l1[key]
        
        # Gestionar tamaño de cache L2
        if len(self.cache_l2) > 500:
            # Eliminar más antiguos
            items_eliminar = list(self.cache_l2.keys())[:200]
            for key in items_eliminar:
                del self.cache_l2[key]
```

### 2. **Pool de Conexiones y Workers**

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import asyncio

class PoolOptimizado:
    def __init__(self):
        # Pool principal para predicciones
        self.pool_predicciones = ThreadPoolExecutor(
            max_workers=4,
            thread_name_prefix="prediccion"
        )
        
        # Pool para tareas I/O (logging, etc.)
        self.pool_io = ThreadPoolExecutor(
            max_workers=2,
            thread_name_prefix="io"
        )
        
        # Semáforo para controlar concurrencia
        self.semaforo_predicciones = threading.Semaphore(4)
        
    def procesar_prediccion_async(self, datos):
        """Procesa predicción de forma asíncrona"""
        future = self.pool_predicciones.submit(
            self.procesar_prediccion_worker,
            datos
        )
        return future
    
    def procesar_prediccion_worker(self, datos):
        """Worker optimizado para predicciones"""
        try:
            self.semaforo_predicciones.acquire()
            
            # Procesamiento real
            resultado = self.ejecutar_prediccion(datos)
            
            # Logging asíncrono
            self.pool_io.submit(self.log_resultado_async, resultado)
            
            return resultado
            
        finally:
            self.semaforo_predicciones.release()
    
    def procesar_lote_predicciones(self, lote_datos):
        """Procesa múltiples predicciones en paralelo"""
        futures = []
        
        for datos in lote_datos:
            future = self.procesar_prediccion_async(datos)
            futures.append(future)
        
        # Recopilar resultados
        resultados = []
        for future in as_completed(futures, timeout=10):
            try:
                resultado = future.result()
                resultados.append(resultado)
            except Exception as e:
                logging.error(f"Error en predicción de lote: {e}")
                resultados.append(None)
        
        return resultados
```

### 3. **Optimización de Modelos ML**

```python
class ModeloOptimizado:
    def __init__(self):
        self.modelo_compilado = None
        self.feature_names_optimized = None
        self.preprocessing_pipeline_fast = None
        
    def optimizar_modelo_carga(self):
        """Optimiza modelo para carga rápida"""
        
        # 1. Cargar modelo una sola vez
        if self.modelo_compilado is None:
            # Cargar con optimizaciones específicas
            self.modelo_compilado = self.cargar_modelo_con_optimizaciones()
            
        # 2. Pre-compilar pipeline de preprocessing
        self.preprocessing_pipeline_fast = self.crear_pipeline_rapido()
        
        # 3. Pre-calcular transformaciones comunes
        self.precalcular_transformaciones()
    
    def predecir_batch_optimizado(self, lote_datos):
        """Predicción optimizada para lotes"""
        
        # Procesamiento vectorizado
        datos_procesados = self.preprocessing_pipeline_fast.transform(lote_datos)
        
        # Predicción en lote (más eficiente que individual)
        predicciones = self.modelo_compilado.predict(datos_procesados)
        probabilidades = self.modelo_compilado.predict_proba(datos_procesados)
        
        # Formatear resultados
        resultados = []
        for i, (pred, prob) in enumerate(zip(predicciones, probabilidades)):
            resultado = {
                'prediccion': int(pred),
                'probabilidades': prob.tolist(),
                'confianza': float(np.max(prob))
            }
            resultados.append(resultado)
        
        return resultados
```

---

## 📈 MONITOREO EN TIEMPO REAL

### Dashboard de Métricas en Vivo

```python
class DashboardTiempoReal:
    def __init__(self):
        self.metricas_actuales = {}
        self.historial_metricas = []
        self.alertas_activas = []
        self.websocket_clients = set()
        
    def actualizar_metricas_tiempo_real(self):
        """Actualiza métricas cada segundo"""
        while True:
            timestamp = time.time()
            
            # Recopilar métricas del sistema
            metricas = {
                'timestamp': timestamp,
                'predicciones_por_segundo': self.calcular_pps(),
                'tiempo_respuesta_promedio': self.calcular_tiempo_promedio(),
                'uso_memoria': self.obtener_uso_memoria(),
                'uso_cpu': self.obtener_uso_cpu(),
                'cache_hit_rate': self.calcular_cache_hit_rate(),
                'errores_por_minuto': self.calcular_errores_por_minuto(),
                'conexiones_activas': len(self.websocket_clients)
            }
            
            # Actualizar métricas actuales
            self.metricas_actuales = metricas
            
            # Agregar a historial (mantener últimas 1000)
            self.historial_metricas.append(metricas)
            if len(self.historial_metricas) > 1000:
                self.historial_metricas.pop(0)
            
            # Verificar alertas
            self.verificar_alertas(metricas)
            
            # Enviar a clientes WebSocket
            self.broadcast_metricas(metricas)
            
            time.sleep(1)  # Actualizar cada segundo
    
    def verificar_alertas(self, metricas):
        """Verifica condiciones de alerta"""
        alertas_nuevas = []
        
        # Alerta: Tiempo de respuesta alto
        if metricas['tiempo_respuesta_promedio'] > 3.0:
            alertas_nuevas.append({
                'tipo': 'warning',
                'mensaje': f"Tiempo de respuesta alto: {metricas['tiempo_respuesta_promedio']:.2f}s",
                'timestamp': time.time()
            })
        
        # Alerta: Uso de memoria alto
        if metricas['uso_memoria'] > 85:
            alertas_nuevas.append({
                'tipo': 'critical',
                'mensaje': f"Uso de memoria crítico: {metricas['uso_memoria']}%",
                'timestamp': time.time()
            })
        
        # Alerta: Cache hit rate bajo
        if metricas['cache_hit_rate'] < 0.3:
            alertas_nuevas.append({
                'tipo': 'info',
                'mensaje': f"Cache hit rate bajo: {metricas['cache_hit_rate']:.1%}",
                'timestamp': time.time()
            })
        
        # Agregar nuevas alertas
        self.alertas_activas.extend(alertas_nuevas)
        
        # Mantener solo últimas 50 alertas
        if len(self.alertas_activas) > 50:
            self.alertas_activas = self.alertas_activas[-50:]

@app.route('/api/metricas-tiempo-real')
def obtener_metricas_tiempo_real():
    """API para obtener métricas en tiempo real"""
    dashboard = DashboardTiempoReal()
    
    return jsonify({
        'metricas_actuales': dashboard.metricas_actuales,
        'historial_ultimo_minuto': dashboard.historial_metricas[-60:],
        'alertas_activas': dashboard.alertas_activas[-10:],
        'estado_sistema': dashboard.evaluar_estado_sistema()
    })
```

### WebSocket para Actualizaciones en Vivo

```javascript
// Frontend: Conexión WebSocket para métricas en tiempo real
class MonitorTiempoReal {
    constructor() {
        this.ws = null;
        this.charts = {};
        this.conectar();
    }
    
    conectar() {
        this.ws = new WebSocket('ws://127.0.0.1:5000/ws/metricas');
        
        this.ws.onopen = () => {
            console.log('Conectado al monitor de tiempo real');
            this.inicializarCharts();
        };
        
        this.ws.onmessage = (event) => {
            const metricas = JSON.parse(event.data);
            this.actualizarCharts(metricas);
            this.actualizarAlertas(metricas.alertas);
        };
        
        this.ws.onclose = () => {
            console.log('Desconectado del monitor');
            // Reconectar después de 5 segundos
            setTimeout(() => this.conectar(), 5000);
        };
        
        this.ws.onerror = (error) => {
            console.error('Error en WebSocket:', error);
        };
    }
    
    actualizarCharts(metricas) {
        // Actualizar gráfico de predicciones por segundo
        this.charts.pps.addPoint([
            metricas.timestamp * 1000,
            metricas.predicciones_por_segundo
        ], true, true);
        
        // Actualizar gráfico de tiempo de respuesta
        this.charts.tiempo_respuesta.addPoint([
            metricas.timestamp * 1000,
            metricas.tiempo_respuesta_promedio
        ], true, true);
        
        // Actualizar métricas numéricas
        document.getElementById('uso-memoria').textContent = 
            metricas.uso_memoria + '%';
        document.getElementById('cache-hit-rate').textContent = 
            (metricas.cache_hit_rate * 100).toFixed(1) + '%';
    }
}

// Inicializar monitor al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const monitor = new MonitorTiempoReal();
});
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### Configuración de Performance

```python
# config/tiempo_real.py
class ConfigTiempoReal:
    # Configuración de Cache
    CACHE_L1_SIZE = 100
    CACHE_L2_SIZE = 500
    CACHE_TTL_SECONDS = 300
    
    # Configuración de Workers
    MAX_WORKERS_PREDICCION = 4
    MAX_WORKERS_IO = 2
    QUEUE_SIZE = 1000
    
    # Configuración de Timeouts
    TIMEOUT_PREDICCION = 5.0
    TIMEOUT_VALIDACION = 1.0
    TIMEOUT_LOGGING = 0.5
    
    # Configuración de Monitoreo
    INTERVALO_METRICAS = 1.0
    HISTORIA_METRICAS = 1000
    MAX_ALERTAS = 50
    
    # Configuración de Memoria
    LIMITE_MEMORIA_PERCENT = 85
    LIMITE_CPU_PERCENT = 80
    INTERVALO_LIMPIEZA = 300
    
    # Configuración de Logs
    LOG_BUFFER_SIZE = 100
    LOG_FLUSH_INTERVAL = 10
    LOG_ROTATION_SIZE = '10MB'
    
    @classmethod
    def cargar_desde_archivo(cls, archivo_config):
        """Carga configuración desde archivo JSON"""
        import json
        
        with open(archivo_config, 'r') as f:
            config_dict = json.load(f)
        
        for key, value in config_dict.items():
            if hasattr(cls, key.upper()):
                setattr(cls, key.upper(), value)
    
    @classmethod
    def optimizar_para_hardware(cls):
        """Optimiza configuración según hardware disponible"""
        import psutil
        
        # Ajustar workers según CPUs disponibles
        cpu_count = psutil.cpu_count()
        cls.MAX_WORKERS_PREDICCION = min(cpu_count, 8)
        
        # Ajustar cache según memoria disponible
        memoria_gb = psutil.virtual_memory().total / (1024**3)
        if memoria_gb >= 8:
            cls.CACHE_L1_SIZE = 200
            cls.CACHE_L2_SIZE = 1000
        elif memoria_gb >= 4:
            cls.CACHE_L1_SIZE = 100
            cls.CACHE_L2_SIZE = 500
        else:
            cls.CACHE_L1_SIZE = 50
            cls.CACHE_L2_SIZE = 200
```

### Variables de Entorno

```bash
# .env - Configuración de producción
# Configuración de Flask
FLASK_ENV=production
FLASK_DEBUG=False

# Configuración de Workers
MAX_WORKERS=4
QUEUE_SIZE=1000

# Configuración de Cache
ENABLE_CACHE=True
CACHE_SIZE_L1=100
CACHE_SIZE_L2=500

# Configuración de Logging
LOG_LEVEL=INFO
LOG_ROTATION=True
LOG_SIZE_LIMIT=10MB

# Configuración de Monitoreo
ENABLE_METRICS=True
METRICS_INTERVAL=1
WEBSOCKET_ENABLED=True

# Configuración de Seguridad
RATE_LIMIT_ENABLED=True
RATE_LIMIT_PER_MINUTE=60
```

---

## 🚨 MANEJO DE ERRORES EN TIEMPO REAL

### Sistema de Recuperación Automática

```python
class RecuperacionTiempoReal:
    def __init__(self):
        self.estado_sistema = "normal"
        self.intentos_recuperacion = {}
        self.max_intentos = 3
        
    def manejar_error_tiempo_real(self, error, contexto):
        """Maneja errores en tiempo real con recuperación automática"""
        
        error_id = f"{type(error).__name__}_{hash(str(error))}"
        timestamp = time.time()
        
        # Registrar intento de recuperación
        if error_id not in self.intentos_recuperacion:
            self.intentos_recuperacion[error_id] = {
                'count': 0,
                'first_occurrence': timestamp,
                'last_attempt': timestamp
            }
        
        intento = self.intentos_recuperacion[error_id]
        intento['count'] += 1
        intento['last_attempt'] = timestamp
        
        # Determinar estrategia de recuperación
        if intento['count'] <= self.max_intentos:
            return self.ejecutar_recuperacion(error, contexto, intento['count'])
        else:
            return self.escalar_error(error, contexto)
    
    def ejecutar_recuperacion(self, error, contexto, intento_numero):
        """Ejecuta estrategia de recuperación según el intento"""
        
        estrategias = {
            1: self.recuperacion_rapida,
            2: self.recuperacion_media,
            3: self.recuperacion_completa
        }
        
        estrategia = estrategias.get(intento_numero, self.escalar_error)
        
        try:
            logging.warning(f"Ejecutando recuperación nivel {intento_numero} para {type(error).__name__}")
            resultado = estrategia(error, contexto)
            
            if resultado:
                # Recuperación exitosa
                error_id = f"{type(error).__name__}_{hash(str(error))}"
                del self.intentos_recuperacion[error_id]
                logging.info(f"Recuperación exitosa en intento {intento_numero}")
            
            return resultado
            
        except Exception as e:
            logging.error(f"Error en recuperación nivel {intento_numero}: {e}")
            return False
    
    def recuperacion_rapida(self, error, contexto):
        """Recuperación rápida - reintentar operación"""
        try:
            # Limpiar cache relevante
            self.limpiar_cache_relacionado(contexto)
            
            # Reintenta operación con timeout reducido
            resultado = self.reintentar_operacion(contexto, timeout=1.0)
            return resultado
            
        except Exception:
            return False
    
    def recuperacion_media(self, error, contexto):
        """Recuperación media - recargar componentes"""
        try:
            # Recargar modelo si es necesario
            if "modelo" in str(error).lower():
                self.recargar_modelo_rapido()
            
            # Limpiar todos los caches
            self.limpiar_todos_los_caches()
            
            # Reintentar con timeout normal
            resultado = self.reintentar_operacion(contexto, timeout=2.0)
            return resultado
            
        except Exception:
            return False
    
    def recuperacion_completa(self, error, contexto):
        """Recuperación completa - reinicializar sistema"""
        try:
            # Reinicializar componentes críticos
            self.reinicializar_componentes_criticos()
            
            # Reintentar operación
            resultado = self.reintentar_operacion(contexto, timeout=5.0)
            return resultado
            
        except Exception:
            return False

# Decorador para manejo automático de errores
def con_recuperacion_automatica(func):
    """Decorador para funciones críticas con recuperación automática"""
    def wrapper(*args, **kwargs):
        recuperador = RecuperacionTiempoReal()
        
        try:
            return func(*args, **kwargs)
        except Exception as e:
            contexto = {
                'funcion': func.__name__,
                'args': args,
                'kwargs': kwargs,
                'timestamp': time.time()
            }
            
            # Intentar recuperación automática
            if recuperador.manejar_error_tiempo_real(e, contexto):
                # Reintentar función original
                return func(*args, **kwargs)
            else:
                # Si no se puede recuperar, propagar error
                raise
    
    return wrapper

# Uso del decorador
@con_recuperacion_automatica
def predecir_con_recuperacion(datos):
    """Función de predicción con recuperación automática"""
    return modelo.predict(datos)
```

---

## 📊 MÉTRICAS Y KPIS

### KPIs de Tiempo Real

```python
class KPIsTiempoReal:
    def __init__(self):
        self.metricas = {
            # Performance
            'tiempo_respuesta_p50': 0,
            'tiempo_respuesta_p95': 0,
            'tiempo_respuesta_p99': 0,
            'throughput_predicciones_por_segundo': 0,
            
            # Calidad
            'tasa_exito': 0,
            'tasa_error': 0,
            'tasa_timeout': 0,
            'cache_hit_rate': 0,
            
            # Recursos
            'uso_cpu_promedio': 0,
            'uso_memoria_promedio': 0,
            'conexiones_concurrentes': 0,
            'queue_size_promedio': 0,
            
            # Business
            'predicciones_totales_dia': 0,
            'ratio_morosos_no_morosos': 0,
            'confianza_promedio_predicciones': 0
        }
        
        self.historial_tiempos = []
        self.ventana_tiempo = 300  # 5 minutos
        
    def registrar_prediccion(self, tiempo_respuesta, resultado, error=None):
        """Registra una predicción para calcular métricas"""
        timestamp = time.time()
        
        # Agregar a historial
        self.historial_tiempos.append({
            'timestamp': timestamp,
            'tiempo_respuesta': tiempo_respuesta,
            'exitosa': error is None,
            'resultado': resultado
        })
        
        # Mantener solo última ventana de tiempo
        tiempo_limite = timestamp - self.ventana_tiempo
        self.historial_tiempos = [
            record for record in self.historial_tiempos
            if record['timestamp'] > tiempo_limite
        ]
        
        # Recalcular métricas
        self.calcular_metricas()
    
    def calcular_metricas(self):
        """Calcula todas las métricas basadas en historial reciente"""
        if not self.historial_tiempos:
            return
        
        # Extraer tiempos de respuesta de predicciones exitosas
        tiempos_exitosos = [
            record['tiempo_respuesta'] 
            for record in self.historial_tiempos 
            if record['exitosa']
        ]
        
        if tiempos_exitosos:
            # Percentiles de tiempo de respuesta
            tiempos_ordenados = sorted(tiempos_exitosos)
            n = len(tiempos_ordenados)
            
            self.metricas['tiempo_respuesta_p50'] = tiempos_ordenados[int(n * 0.5)]
            self.metricas['tiempo_respuesta_p95'] = tiempos_ordenados[int(n * 0.95)]
            self.metricas['tiempo_respuesta_p99'] = tiempos_ordenados[int(n * 0.99)]
        
        # Tasas de éxito/error
        total_predicciones = len(self.historial_tiempos)
        predicciones_exitosas = sum(1 for r in self.historial_tiempos if r['exitosa'])
        
        self.metricas['tasa_exito'] = predicciones_exitosas / total_predicciones
        self.metricas['tasa_error'] = 1 - self.metricas['tasa_exito']
        
        # Throughput
        tiempo_ventana = self.ventana_tiempo
        self.metricas['throughput_predicciones_por_segundo'] = total_predicciones / tiempo_ventana
        
        # Métricas de negocio
        resultados_validos = [r['resultado'] for r in self.historial_tiempos if r['exitosa'] and r['resultado']]
        
        if resultados_validos:
            morosos = sum(1 for r in resultados_validos if r.get('prediccion') == 1)
            no_morosos = sum(1 for r in resultados_validos if r.get('prediccion') == 0)
            
            if no_morosos > 0:
                self.metricas['ratio_morosos_no_morosos'] = morosos / no_morosos
            
            # Confianza promedio
            confianzas = [r.get('confianza', 0) for r in resultados_validos]
            if confianzas:
                self.metricas['confianza_promedio_predicciones'] = sum(confianzas) / len(confianzas)
    
    def generar_reporte_kpis(self):
        """Genera reporte completo de KPIs"""
        return {
            'timestamp': time.time(),
            'periodo_analisis_minutos': self.ventana_tiempo / 60,
            'total_predicciones_analizadas': len(self.historial_tiempos),
            'metricas': self.metricas,
            'estado_performance': self.evaluar_estado_performance(),
            'recomendaciones': self.generar_recomendaciones()
        }
    
    def evaluar_estado_performance(self):
        """Evalúa el estado general de performance"""
        problemas = []
        
        if self.metricas['tiempo_respuesta_p95'] > 3.0:
            problemas.append("Tiempo de respuesta P95 alto")
        
        if self.metricas['tasa_error'] > 0.05:
            problemas.append("Tasa de error alta")
        
        if self.metricas['throughput_predicciones_por_segundo'] < 1.0:
            problemas.append("Throughput bajo")
        
        if not problemas:
            return "EXCELENTE"
        elif len(problemas) == 1:
            return "BUENO"
        elif len(problemas) == 2:
            return "REGULAR"
        else:
            return "CRITICO"
```

### Dashboard de KPIs en Tiempo Real

```html
<!-- dashboard_tiempo_real.html -->
<div id="dashboard-tiempo-real" class="dashboard-container">
    <div class="metricas-principales">
        <div class="metrica-card">
            <h3>⚡ Tiempo Respuesta</h3>
            <div class="metrica-valor" id="tiempo-p95">0.0s</div>
            <div class="metrica-detalle">P95</div>
        </div>
        
        <div class="metrica-card">
            <h3>📊 Throughput</h3>
            <div class="metrica-valor" id="throughput">0.0</div>
            <div class="metrica-detalle">pred/seg</div>
        </div>
        
        <div class="metrica-card">
            <h3>✅ Tasa Éxito</h3>
            <div class="metrica-valor" id="tasa-exito">0.0%</div>
            <div class="metrica-detalle">últimos 5min</div>
        </div>
        
        <div class="metrica-card">
            <h3>🎯 Confianza</h3>
            <div class="metrica-valor" id="confianza-promedio">0.0%</div>
            <div class="metrica-detalle">promedio</div>
        </div>
    </div>
    
    <div class="graficos-tiempo-real">
        <div class="grafico-container">
            <canvas id="chart-tiempo-respuesta"></canvas>
        </div>
        
        <div class="grafico-container">
            <canvas id="chart-throughput"></canvas>
        </div>
    </div>
    
    <div class="alertas-tiempo-real" id="alertas-container">
        <!-- Alertas se insertan dinámicamente -->
    </div>
</div>

<script>
class DashboardTiempoReal {
    constructor() {
        this.charts = {};
        this.websocket = null;
        this.inicializar();
    }
    
    inicializar() {
        this.crearCharts();
        this.conectarWebSocket();
        this.iniciarActualizacionPeriodica();
    }
    
    crearCharts() {
        // Chart de tiempo de respuesta
        const ctx1 = document.getElementById('chart-tiempo-respuesta').getContext('2d');
        this.charts.tiempoRespuesta = new Chart(ctx1, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Tiempo Respuesta (s)',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 5
                    }
                },
                animation: false
            }
        });
        
        // Chart de throughput
        const ctx2 = document.getElementById('chart-throughput').getContext('2d');
        this.charts.throughput = new Chart(ctx2, {
            type: 'bar',
            data: {
                labels: [],
                datasets: [{
                    label: 'Predicciones/seg',
                    data: [],
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                animation: false
            }
        });
    }
    
    conectarWebSocket() {
        this.websocket = new WebSocket('ws://127.0.0.1:5000/ws/kpis');
        
        this.websocket.onmessage = (event) => {
            const kpis = JSON.parse(event.data);
            this.actualizarDashboard(kpis);
        };
        
        this.websocket.onclose = () => {
            setTimeout(() => this.conectarWebSocket(), 5000);
        };
    }
    
    actualizarDashboard(kpis) {
        // Actualizar métricas principales
        document.getElementById('tiempo-p95').textContent = 
            kpis.metricas.tiempo_respuesta_p95.toFixed(2) + 's';
        document.getElementById('throughput').textContent = 
            kpis.metricas.throughput_predicciones_por_segundo.toFixed(1);
        document.getElementById('tasa-exito').textContent = 
            (kpis.metricas.tasa_exito * 100).toFixed(1) + '%';
        document.getElementById('confianza-promedio').textContent = 
            (kpis.metricas.confianza_promedio_predicciones * 100).toFixed(1) + '%';
        
        // Actualizar charts
        this.actualizarChart('tiempoRespuesta', 
            kpis.metricas.tiempo_respuesta_p95);
        this.actualizarChart('throughput', 
            kpis.metricas.throughput_predicciones_por_segundo);
        
        // Actualizar alertas si hay problemas
        if (kpis.estado_performance !== 'EXCELENTE') {
            this.mostrarAlerta(kpis.estado_performance, kpis.recomendaciones);
        }
    }
    
    actualizarChart(chartName, valor) {
        const chart = this.charts[chartName];
        const now = new Date().toLocaleTimeString();
        
        // Agregar nuevo punto
        chart.data.labels.push(now);
        chart.data.datasets[0].data.push(valor);
        
        // Mantener solo últimos 20 puntos
        if (chart.data.labels.length > 20) {
            chart.data.labels.shift();
            chart.data.datasets[0].data.shift();
        }
        
        chart.update();
    }
}

// Inicializar dashboard al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    new DashboardTiempoReal();
});
</script>
```

---

**📋 Resumen del Procesamiento en Tiempo Real:**

✅ **Arquitectura Optimizada**: Pipeline de < 2 segundos end-to-end
✅ **Caching Inteligente**: Multinivel con alta tasa de hits
✅ **Procesamiento Concurrente**: Workers optimizados para carga
✅ **Monitoreo Continuo**: Métricas y KPIs en tiempo real
✅ **Recuperación Automática**: Manejo inteligente de errores
✅ **Escalabilidad**: Configuración adaptable al hardware
✅ **Dashboard en Vivo**: Visualización de performance instantánea

*El sistema está diseñado para procesar miles de predicciones diarias manteniendo tiempos de respuesta consistentemente bajos y alta disponibilidad.*

**Última actualización:** 28 de Octubre, 2025