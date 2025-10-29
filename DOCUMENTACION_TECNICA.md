# Documentación Técnica
## Sistema de Predicción de Morosidad - Ahorro Valle

**Versión**: 1.0  
**Fecha**: 28 de Octubre, 2025  
**Autor**: Carmen Mendez  

---

## Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Componentes del Proyecto](#componentes-del-proyecto)
4. [Modelo de Machine Learning](#modelo-de-machine-learning)
5. [API y Endpoints](#api-y-endpoints)
6. [Interfaz de Usuario](#interfaz-de-usuario)
7. [Flujo de Datos](#flujo-de-datos)
8. [Seguridad y Validaciones](#seguridad-y-validaciones)
9. [Instalación y Configuración](#instalación-y-configuración)
10. [Testing y Calidad](#testing-y-calidad)
11. [Mantenimiento](#mantenimiento)
12. [Troubleshooting](#troubleshooting)

---

## Resumen Ejecutivo

### Objetivo del Proyecto
Sistema web de predicción de riesgo crediticio que utiliza Machine Learning para evaluar automáticamente la probabilidad de morosidad de solicitantes de préstamos en Ahorro Valle.

### Tecnologías Core
- **Backend**: Python 3.13.2, Flask 3.1.0
- **Machine Learning**: Scikit-learn 1.7.2, Pandas 2.3.3, NumPy 2.3.4
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Almacenamiento**: JSON (logs), Joblib (modelos), CSV (datasets)

### Métricas del Modelo
- **Algoritmo**: Regresión Logística Optimizada
- **Accuracy**: 61.8% en conjunto de prueba
- **Precision**: 65.2%
- **Recall**: 58.4%
- **F1-Score**: 61.6%
- **ROC-AUC**: 0.673

---

## Arquitectura del Sistema

### Diagrama de Arquitectura
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    FRONTEND     │    │     BACKEND     │    │   MODELO ML     │
│                 │    │                 │    │                 │
│ • HTML/CSS/JS   │◄──►│ • Flask API     │◄──►│ • Scikit-learn  │
│ • Formularios   │    │ • Validaciones  │    │ • Pipeline      │
│ • Visualización │    │ • Lógica        │    │ • Preprocessor  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                ▼
                       ┌─────────────────┐
                       │    STORAGE      │
                       │                 │
                       │ • JSON Logs     │
                       │ • Joblib Models │
                       │ • CSV Datasets  │
                       └─────────────────┘
```

### Patrón de Diseño
**MVC (Model-View-Controller)**:
- **Model**: Modelo ML + Lógica de datos
- **View**: Templates HTML + CSS/JS
- **Controller**: Flask routes + Business logic

### Stack Tecnológico

#### Backend
```python
Flask==3.1.0           # Framework web
scikit-learn==1.7.2    # Machine Learning
pandas==2.3.3          # Manipulación de datos
numpy==2.3.4           # Computación científica
joblib==1.5.2          # Serialización de modelos
```

#### Frontend
```html
HTML5                  # Estructura
CSS3                   # Estilos responsivos
JavaScript ES6         # Interactividad
Bootstrap (CDN)        # Framework CSS
```

---

## Componentes del Proyecto

### Estructura de Directorios
```
AhorroValle/
├── app.py                              # Aplicación Flask principal
├── morosidadTrain.py                   # Script de entrenamiento ML
├── dataset_credito_morosidad.csv       # Dataset de entrenamiento
├── requirements.txt                    # Dependencias Python
├── README.md                           # Documentación principal
├── templates/                          # Plantillas HTML
│   ├── index.html                      # Página principal
│   ├── estadisticas.html               # Dashboard
│   ├── demo.html                       # Modo demo
│   └── about.html                      # Información
├── static/                             # Archivos estáticos
│   ├── css/
│   │   └── style.css                   # Estilos principales
│   └── js/
│       └── script.js                   # JavaScript principal
├── output/                             # Artefactos del modelo
│   ├── model_pipeline_final_*.joblib   # Modelos entrenados
│   └── training_results_*.json         # Métricas
├── logs/                               # Logs del sistema
│   └── predicciones_*.json             # Registro predicciones
└── entorno/                            # Entorno virtual
```

### Archivos Principales

#### 1. `app.py` - Servidor Flask
```python
# Funciones principales:
def cargar_modelo_mas_reciente()        # Carga automática del modelo
def predecir()                          # Endpoint de predicción
def clasificar_riesgo()                 # Clasificación de riesgo
def generar_recomendacion()             # Lógica de recomendaciones
def guardar_prediccion_log()            # Registro de predicciones

# Rutas definidas:
@app.route('/')                         # Página principal
@app.route('/predict', methods=['POST']) # API de predicción
@app.route('/estadisticas')             # Dashboard
@app.route('/demo')                     # Modo demo
```

#### 2. `morosidadTrain.py` - Entrenamiento ML
```python
# Clases principales:
class EDA_Morosidad                     # Análisis exploratorio
class ClasificadorMorosidad             # Pipeline ML

# Métodos de optimización:
def _optimizar_mejor_modelo()           # Búsqueda hiperparámetros
def _entrenar_modelo_final()            # Entrenamiento final
def _evaluar_modelo()                   # Evaluación modelo
def _guardar_modelo()                   # Persistencia modelo
```

---

## Modelo de Machine Learning

### Pipeline de Procesamiento
```python
Pipeline([
    ('preprocessor', ColumnTransformer([
        ('num', StandardScaler(), numeric_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features)
    ])),
    ('imputer', SimpleImputer(strategy='median')),
    ('classifier', LogisticRegression(
        C=0.1,
        max_iter=1000,
        random_state=42,
        solver='liblinear'
    ))
])
```

### Características del Modelo

#### Variables de Entrada (17 features)
```python
NUMERIC_FEATURES = [
    'edad', 'antiguedad_laboral', 'ingresos_mensuales',
    'monto_credito', 'plazo_meses', 'valor_garantia',
    'credito_score', 'num_pagos_anteriores', 'num_creditos_anteriores',
    'precio_soya', 'precio_vino', 'uso_productos_financieros'
]

CATEGORICAL_FEATURES = [
    'genero', 'zona_residencia', 'tipo_empleo',
    'destino_credito', 'tipo_garantia'
]
```

#### Rangos de Validación
```python
VALIDATION_RANGES = {
    'edad': (18, 80),
    'ingresos_mensuales': (1_000_000, 50_000_000),
    'monto_credito': (500_000, 100_000_000),
    'plazo_meses': (1, 120),
    'credito_score': (300, 850),
    'antiguedad_laboral': (0, 40),
    'valor_garantia': (0, 500_000_000)
}
```

### Proceso de Entrenamiento

#### 1. Preprocesamiento
```python
# Limpieza de datos
df_clean = df.dropna(subset=['morosidad'])

# Encoding de variables categóricas
df_encoded = pd.get_dummies(df_clean, columns=categorical_features)

# División train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
```

#### 2. Optimización de Hiperparámetros
```python
param_grid = {
    'classifier__C': [0.001, 0.01, 0.1, 1, 10, 100],
    'classifier__solver': ['liblinear', 'lbfgs'],
    'classifier__max_iter': [1000, 2000]
}

grid_search = GridSearchCV(
    pipeline, param_grid, cv=5, 
    scoring='accuracy', n_jobs=-1
)
```

#### 3. Evaluación
```python
# Métricas principales
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
```

---

## API y Endpoints

### Rutas Disponibles

#### 1. Página Principal
```python
@app.route('/')
def index():
    """Página principal con formulario de predicción"""
    return render_template('index.html')
```

#### 2. API de Predicción
```python
@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint principal de predicción
    
    Input: JSON con datos del solicitante
    Output: JSON con predicción, probabilidades y recomendación
    """
```

**Request Format:**
```json
{
    "edad": 35,
    "genero": "Masculino",
    "zona_residencia": "Urbana",
    "tipo_empleo": "Empleado",
    "antiguedad_laboral": 5,
    "ingresos_mensuales": 3000000,
    "monto_credito": 15000000,
    "plazo_meses": 24,
    "destino_credito": "Vivienda",
    "tipo_garantia": "Hipotecaria",
    "valor_garantia": 25000000,
    "credito_score": 650,
    "num_pagos_anteriores": 12,
    "num_creditos_anteriores": 3,
    "precio_soya": 1500,
    "precio_vino": 8000,
    "uso_productos_financieros": 2
}
```

**Response Format:**
```json
{
    "prediccion": "NO MOROSO",
    "probabilidades": {
        "no_moroso": 0.725,
        "moroso": 0.275
    },
    "clasificacion_riesgo": "BAJO",
    "recomendacion": "APROBAR - Riesgo bajo, perfil crediticio favorable",
    "factores_principales": [
        "Credit Score alto (650)",
        "Ingresos estables y suficientes",
        "Buena garantía hipotecaria"
    ],
    "timestamp": "2025-01-28T14:30:25",
    "tiempo_procesamiento": 0.156
}
```

#### 3. Dashboard de Estadísticas
```python
@app.route('/estadisticas')
def estadisticas():
    """Dashboard con métricas del sistema"""
    return render_template('estadisticas.html')
```

#### 4. Modo Demo
```python
@app.route('/demo')
def demo():
    """Página de demostración con casos predefinidos"""
    return render_template('demo.html')
```

### Validación de API

#### Validación Frontend (JavaScript)
```javascript
function validarDatos(formData) {
    const errores = [];
    
    // Validar campos requeridos
    const camposRequeridos = ['edad', 'ingresos_mensuales', 'monto_credito'];
    camposRequeridos.forEach(campo => {
        if (!formData[campo] || formData[campo] === '') {
            errores.push(`Campo requerido: ${campo}`);
        }
    });
    
    // Validar rangos
    if (formData.edad < 18 || formData.edad > 80) {
        errores.push('Edad debe estar entre 18 y 80 años');
    }
    
    return errores;
}
```

#### Validación Backend (Python)
```python
def validar_datos_entrada(data):
    errores = []
    
    # Validar presencia de campos
    campos_requeridos = ['edad', 'ingresos_mensuales', 'monto_credito']
    for campo in campos_requeridos:
        if campo not in data:
            errores.append(f"Campo faltante: {campo}")
    
    # Validar tipos y rangos
    try:
        edad = int(data.get('edad', 0))
        if not (18 <= edad <= 80):
            errores.append("Edad debe estar entre 18 y 80")
    except ValueError:
        errores.append("Edad debe ser un número")
    
    return errores
```

---

## Interfaz de Usuario

### Diseño Responsivo

#### CSS Framework
```css
/* Variables CSS para consistencia */
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e293b;
    --success-color: #059669;
    --warning-color: #d97706;
    --danger-color: #dc2626;
    --font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Layout responsive */
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

@media (max-width: 768px) {
    .container {
        padding: 0 10px;
    }
}
```

#### Componentes UI

**Formulario de Predicción:**
```html
<form id="prediction-form" class="prediction-form">
    <div class="form-section">
        <h3>Datos Personales</h3>
        <div class="form-row">
            <input type="text" name="edad" placeholder="Edad" required>
            <select name="genero" required>
                <option value="">Seleccionar Género</option>
                <option value="Masculino">Masculino</option>
                <option value="Femenino">Femenino</option>
            </select>
        </div>
    </div>
</form>
```

**Resultado de Predicción:**
```html
<div class="result-container" id="result">
    <div class="prediction-result">
        <h2 class="result-title">Resultado: <span id="prediction"></span></h2>
        <div class="probabilities">
            <div class="prob-item">
                <span>No Moroso:</span>
                <span id="prob-no-moroso"></span>
            </div>
        </div>
        <div class="risk-classification">
            <span class="risk-label" id="risk-level"></span>
        </div>
        <div class="recommendation">
            <p id="recommendation-text"></p>
        </div>
    </div>
</div>
```

### JavaScript Interactivo

#### Manejo de Formularios
```javascript
document.getElementById('prediction-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    try {
        showLoading();
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        displayResult(result);
    } catch (error) {
        showError('Error al procesar la predicción');
    } finally {
        hideLoading();
    }
});
```

#### Visualización de Resultados
```javascript
function displayResult(result) {
    document.getElementById('prediction').textContent = result.prediccion;
    document.getElementById('prob-no-moroso').textContent = 
        `${(result.probabilidades.no_moroso * 100).toFixed(1)}%`;
    
    const riskElement = document.getElementById('risk-level');
    riskElement.textContent = result.clasificacion_riesgo;
    riskElement.className = `risk-label risk-${result.clasificacion_riesgo.toLowerCase()}`;
    
    document.getElementById('recommendation-text').textContent = result.recomendacion;
}
```

---

## Flujo de Datos

### Diagrama de Flujo de Predicción
```
Usuario → Formulario → Validación Frontend → API Request → 
Validación Backend → Modelo ML → Clasificación Riesgo → 
Recomendación → Log → Response → UI Update
```

### Procesamiento Detallado

#### 1. Captura de Datos
```javascript
// Frontend: Captura y validación inicial
const formData = new FormData(document.getElementById('prediction-form'));
const validationErrors = validateForm(formData);
if (validationErrors.length > 0) {
    showErrors(validationErrors);
    return;
}
```

#### 2. Envío a Backend
```python
# Backend: Recepción y validación
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    
    # Validar datos
    errors = validar_datos_entrada(data)
    if errors:
        return jsonify({'errors': errors}), 400
```

#### 3. Preprocesamiento
```python
# Conversión de tipos
processed_data = {}
for key, value in data.items():
    if key in numeric_fields:
        processed_data[key] = float(value)
    else:
        processed_data[key] = str(value)

# Crear DataFrame para modelo
df_input = pd.DataFrame([processed_data])
```

#### 4. Predicción
```python
# Aplicar modelo
probability = modelo.predict_proba(df_input)[0]
prediction = modelo.predict(df_input)[0]

# Clasificar riesgo
riesgo = clasificar_riesgo(probability[1])
recomendacion = generar_recomendacion(prediction, probability, data)
```

#### 5. Logging
```python
# Guardar predicción
log_entry = {
    'timestamp': datetime.now().isoformat(),
    'input_data': data,
    'prediction': prediction,
    'probabilities': probability.tolist(),
    'risk_level': riesgo,
    'recommendation': recomendacion
}

guardar_prediccion_log(log_entry)
```

---

## Seguridad y Validaciones

### Validación por Capas

#### 1. Validación Frontend
- Campos requeridos
- Tipos de datos básicos
- Rangos simples
- Formato de entrada

#### 2. Validación Backend
- Validación exhaustiva de tipos
- Rangos de negocio
- Sanitización de entrada
- Validación de consistencia

#### 3. Validación ML
- Shape de datos
- Características esperadas
- Detección de outliers
- Validación de resultado

### Medidas de Seguridad

#### Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour", "10 per minute"]
)

@app.route('/predict', methods=['POST'])
@limiter.limit("5 per minute")
def predict():
    # Código de predicción
```

#### Sanitización de Entrada
```python
import html
import re

def sanitizar_entrada(data):
    sanitized = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Escapar HTML
            value = html.escape(value)
            # Remover caracteres especiales
            value = re.sub(r'[<>"\']', '', value)
        sanitized[key] = value
    return sanitized
```

#### Logging de Seguridad
```python
import logging

security_logger = logging.getLogger('security')

def log_security_event(event_type, details):
    security_logger.warning(f"Security Event: {event_type} - {details}")

# Ejemplo de uso
if len(errors) > 5:
    log_security_event("MULTIPLE_VALIDATION_ERRORS", 
                      f"IP: {request.remote_addr}")
```

---

## Instalación y Configuración

### Requisitos del Sistema
- **Python**: 3.8 o superior
- **RAM**: Mínimo 4GB, recomendado 8GB
- **Disco**: 2GB de espacio libre
- **SO**: Windows 10/11, macOS 10.14+, Ubuntu 18.04+

### Instalación Paso a Paso

#### 1. Clonar Repositorio
```bash
git clone https://github.com/carmendez-dev/Predicci-n-de-morosidad-en-Cooperativa.git
cd Predicci-n-de-morosidad-en-Cooperativa
```

#### 2. Crear Entorno Virtual
```bash
python -m venv entorno

# Windows
entorno\Scripts\activate

# macOS/Linux
source entorno/bin/activate
```

#### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 4. Entrenar Modelo
```bash
python morosidadTrain.py
```

#### 5. Iniciar Aplicación
```bash
python app.py
```

### Configuración de Producción

#### Variables de Entorno
```bash
export FLASK_ENV=production
export FLASK_DEBUG=False
export MODEL_PATH=/path/to/models
export LOG_LEVEL=INFO
```

#### Configuración de Servidor
```python
# config.py
import os

class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    MODEL_PATH = os.environ.get('MODEL_PATH', 'output/')
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
```

---

## Testing y Calidad

### Tests Automatizados

#### Unit Tests
```python
import unittest
from app import app

class TestPrediccionAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_prediction_endpoint(self):
        """Test del endpoint de predicción"""
        data = {
            'edad': 35,
            'genero': 'Masculino',
            'ingresos_mensuales': 3000000,
            # ... más datos
        }
        
        response = self.app.post('/predict', 
                                json=data,
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        result = response.get_json()
        self.assertIn('prediccion', result)
        self.assertIn('probabilidades', result)
```

#### Integration Tests
```python
def test_complete_prediction_flow(self):
    """Test del flujo completo de predicción"""
    # 1. Enviar datos válidos
    response = self.send_prediction_request(valid_data)
    self.assertEqual(response.status_code, 200)
    
    # 2. Verificar estructura de respuesta
    result = response.get_json()
    self.validate_response_structure(result)
    
    # 3. Verificar que se guardó el log
    self.assertTrue(self.log_exists(result['timestamp']))
```

### Calidad de Código

#### Linting
```bash
# Instalar herramientas
pip install flake8 black

# Ejecutar linting
flake8 app.py morosidadTrain.py

# Formatear código
black app.py morosidadTrain.py
```

#### Code Coverage
```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con coverage
coverage run -m unittest discover tests/
coverage report -m
coverage html
```

---

## Mantenimiento

### Monitoreo del Sistema

#### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    """Endpoint para verificar salud del sistema"""
    try:
        # Verificar modelo cargado
        if modelo is None:
            return jsonify({'status': 'error', 'message': 'Model not loaded'}), 500
        
        # Verificar recursos del sistema
        import psutil
        memory_usage = psutil.virtual_memory().percent
        
        if memory_usage > 90:
            return jsonify({'status': 'warning', 'message': 'High memory usage'}), 200
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'memory_usage': f"{memory_usage:.1f}%"
        }), 200
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
```

#### Logging de Sistema
```python
import logging
from logging.handlers import RotatingFileHandler

# Configurar logging
if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Sistema iniciado')
```

### Actualizaciones del Modelo

#### Re-entrenamiento Periódico
```python
def actualizar_modelo(nuevo_dataset_path):
    """
    Proceso de actualización del modelo
    """
    try:
        # 1. Cargar nuevos datos
        nuevo_df = pd.read_csv(nuevo_dataset_path)
        
        # 2. Validar calidad de datos
        if validar_calidad_datos(nuevo_df):
            
            # 3. Re-entrenar modelo
            nuevo_modelo = entrenar_modelo(nuevo_df)
            
            # 4. Validar performance
            if validar_performance(nuevo_modelo):
                
                # 5. Backup modelo actual
                backup_modelo_actual()
                
                # 6. Deployar nuevo modelo
                deployar_modelo(nuevo_modelo)
                
                return True
        
        return False
        
    except Exception as e:
        app.logger.error(f"Error actualizando modelo: {e}")
        return False
```

---

## Troubleshooting

### Problemas Comunes

#### 1. Modelo No Carga
**Síntomas**: Error 500 al hacer predicciones
**Causas**:
- Archivo de modelo corrupto
- Versión incompatible de scikit-learn
- Ruta incorrecta

**Solución**:
```bash
# Re-entrenar modelo
python morosidadTrain.py

# Verificar versión de librerías
pip list | grep scikit-learn

# Verificar ruta
ls -la output/model_pipeline_final_*.joblib
```

#### 2. Alta Latencia en Predicciones
**Síntomas**: Tiempo de respuesta > 5 segundos
**Causas**:
- Modelo muy complejo
- Falta de memoria
- Procesamiento ineficiente

**Solución**:
```python
# Optimizar carga del modelo
@lru_cache(maxsize=1)
def get_modelo():
    return joblib.load(model_path)

# Usar modelo pre-cargado
modelo = get_modelo()
```

#### 3. Errores de Validación
**Síntomas**: Errores constantes de validación
**Causas**:
- Datos de entrada incorrectos
- Validaciones muy estrictas
- Problemas de encoding

**Solución**:
```python
# Logging detallado de validación
def validar_con_logging(data):
    errores = []
    for campo, valor in data.items():
        try:
            validar_campo(campo, valor)
        except ValidationError as e:
            errores.append(f"{campo}: {e}")
            app.logger.debug(f"Validation error - {campo}: {valor} - {e}")
    return errores
```

### Logs de Diagnóstico

#### Estructura de Logs
```
logs/
├── app.log                    # Log principal de la aplicación
├── predicciones_YYYY-MM-DD.json  # Log de predicciones por día
├── errores.log               # Log específico de errores
└── security.log              # Log de eventos de seguridad
```

#### Análisis de Logs
```bash
# Ver errores recientes
tail -f logs/errores.log

# Contar predicciones del día
grep "$(date +%Y-%m-%d)" logs/predicciones_*.json | wc -l

# Buscar errores específicos
grep "ValidationError" logs/app.log | tail -10
```

---

## Glosario Técnico

**API**: Application Programming Interface - Interfaz para comunicación entre sistemas
**Cross-validation**: Técnica de validación cruzada para evaluar modelos
**Endpoint**: Punto de acceso específico en una API
**F1-Score**: Métrica que combina precision y recall
**Flask**: Framework web ligero para Python
**Joblib**: Librería para serialización eficiente de objetos Python
**Machine Learning**: Aprendizaje automático usando algoritmos
**Pipeline**: Secuencia de pasos de procesamiento de datos
**Precision**: Proporción de predicciones positivas correctas
**Recall**: Proporción de casos positivos correctamente identificados
**ROC-AUC**: Área bajo la curva ROC, métrica de calidad del modelo
**Scikit-learn**: Librería de machine learning para Python

---

**Última actualización**: 28 de Octubre, 2025  
**Versión del documento**: 1.0  
**Mantenido por**: Carmen Mendez - Universidad Católica Boliviana "San Pablo"