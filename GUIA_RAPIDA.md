# 🚀 GUÍA RÁPIDA DE USO

## ▶️ Iniciar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://127.0.0.1:5000**

---

## 📝 Acceso Rápido a las Páginas

- **Predicción:** http://127.0.0.1:5000/
- **Estadísticas:** http://127.0.0.1:5000/estadisticas
- **Información:** http://127.0.0.1:5000/about

---

## 🎯 Realizar una Predicción

### Opción 1: Interfaz Web

1. Abre http://127.0.0.1:5000/ en tu navegador
2. Completa el formulario con los datos del cliente
3. Haz clic en "🔍 Predecir Morosidad"
4. Revisa el resultado

### Opción 2: API (Programáticamente)

```python
import requests

datos = {
    "edad": 35,
    "genero": "M",
    "zona": "Urbana",
    "tipo_empleo": "Dependiente",
    "antiguedad": 8,
    "ingresos": 4500.00,
    "score_crediticio": 720,
    "pagos_previos": 3,
    "creditos_previos": 2,
    "monto_credito": 50000,
    "plazo_meses": 24,
    "destino_credito": "Consumo",
    "tipo_garantia": "Vehiculo",
    "valor_garantia": 55000.00,
    "precio_soya": 420.50,
    "precio_vino": 48.00,
    "uso_productos": 2
}

response = requests.post("http://127.0.0.1:5000/predecir", json=datos)
resultado = response.json()
print(resultado)
```

---

## 📊 Ejemplo de Datos para Prueba

### Cliente de Bajo Riesgo
```json
{
    "edad": 45,
    "genero": "M",
    "zona": "Urbana",
    "tipo_empleo": "Gobierno",
    "antiguedad": 20,
    "ingresos": 8000.00,
    "score_crediticio": 810,
    "pagos_previos": 5,
    "creditos_previos": 8,
    "monto_credito": 30000,
    "plazo_meses": 12,
    "destino_credito": "Consumo",
    "tipo_garantia": "Inmueble",
    "valor_garantia": 120000.00,
    "precio_soya": 430.00,
    "precio_vino": 45.00,
    "uso_productos": 4
}
```

### Cliente de Alto Riesgo
```json
{
    "edad": 22,
    "genero": "F",
    "zona": "Rural",
    "tipo_empleo": "Independiente",
    "antiguedad": 1,
    "ingresos": 2000.00,
    "score_crediticio": 550,
    "pagos_previos": 0,
    "creditos_previos": 0,
    "monto_credito": 80000,
    "plazo_meses": 48,
    "destino_credito": "Comercial",
    "tipo_garantia": "Ninguna",
    "valor_garantia": 10000.00,
    "precio_soya": 380.00,
    "precio_vino": 55.00,
    "uso_productos": 0
}
```

---

## 🧪 Probar la API

Ejecuta el script de prueba incluido:

```bash
python test_api.py
```

Este script probará 3 perfiles diferentes de clientes y mostrará los resultados.

---

## 🔑 Campos Requeridos

### Datos Personales
- `edad`: 18-100
- `genero`: "M" o "F"
- `zona`: "Urbana" o "Rural"

### Información Laboral
- `tipo_empleo`: "Dependiente", "Independiente", "Agricola", "Gobierno"
- `antiguedad`: 0-50 años
- `ingresos`: > 0

### Historial Crediticio
- `score_crediticio`: 300-850
- `pagos_previos`: 0-100
- `creditos_previos`: 0-50

### Crédito Solicitado
- `monto_credito`: > 0
- `plazo_meses`: 6, 12, 24, 36, 48, 60
- `destino_credito`: "Consumo", "Comercial", "Agricola"

### Garantías
- `tipo_garantia`: "Ninguna", "Vehiculo", "Inmueble"
- `valor_garantia`: > 0

### Variables Económicas
- `precio_soya`: > 0
- `precio_vino`: > 0
- `uso_productos`: 0-10

---

## 📈 Interpretación de Resultados

### Predicción
- **0 = NO MOROSO** - Cliente confiable
- **1 = MOROSO** - Alto riesgo de incumplimiento

### Nivel de Riesgo
- **BAJO** (< 20%): Aprobar sin restricciones
- **MEDIO** (20-50%): Aprobar con condiciones estándar
- **ALTO** (50-70%): Requiere garantías adicionales
- **MUY ALTO** (> 70%): Considerar rechazo

---

## 🛑 Detener la Aplicación

Presiona `Ctrl + C` en la terminal donde está corriendo el servidor.

---

## 📁 Archivos Importantes

- `app.py` - Servidor Flask
- `morosidadTrain.py` - Script de entrenamiento
- `test_api.py` - Script de prueba
- `output/model_pipeline_final_*.joblib` - Modelo entrenado
- `logs/predicciones_*.json` - Logs de predicciones

---

## 🐛 Solución Rápida de Problemas

**Problema:** El servidor no inicia
```bash
# Verificar que Flask esté instalado
pip list | findstr Flask

# Si no está, instalar
pip install Flask flask-cors
```

**Problema:** "No se encontró ningún modelo"
```bash
# Entrenar el modelo primero
python morosidadTrain.py
```

**Problema:** Error de conexión
```bash
# Verificar que el servidor esté corriendo
# Debe aparecer: "Running on http://127.0.0.1:5000"
```

---

## 💡 Consejos

✅ Usa valores realistas para mejores predicciones
✅ El score crediticio es uno de los factores más importantes
✅ Revisa las estadísticas para ver patrones
✅ Los logs se guardan automáticamente en `logs/`
✅ Puedes imprimir los resultados desde el navegador

---

**¡Listo para predecir morosidad!** 🎉
