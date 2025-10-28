"""
APLICACIÓN WEB DE PREDICCIÓN DE MOROSIDAD
Sistema web para predecir morosidad crediticia usando el modelo entrenado
"""
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime
import json

app = Flask(__name__)

# Cargar el modelo entrenado más reciente
def cargar_modelo_mas_reciente():
    """Carga el modelo más reciente del directorio output"""
    output_dir = 'output'
    modelos = [f for f in os.listdir(output_dir) if f.startswith('model_pipeline_final') and f.endswith('.joblib')]
    
    if not modelos:
        raise FileNotFoundError("No se encontró ningún modelo entrenado en el directorio 'output'")
    
    # Ordenar por fecha (más reciente primero)
    modelos.sort(reverse=True)
    modelo_path = os.path.join(output_dir, modelos[0])
    
    print(f"Cargando modelo: {modelo_path}")
    return joblib.load(modelo_path), modelos[0]

# Cargar el modelo al iniciar la aplicación
try:
    modelo, modelo_nombre = cargar_modelo_mas_reciente()
    print(f"Modelo cargado exitosamente: {modelo_nombre}")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    modelo = None
    modelo_nombre = None

# Definir las opciones categóricas válidas
OPCIONES_CATEGORICAS = {
    'genero': ['M', 'F'],
    'zona': ['Urbana', 'Rural'],
    'tipo_empleo': ['Dependiente', 'Independiente', 'Agricola', 'Gobierno'],
    'destino_credito': ['Consumo', 'Comercial', 'Agricola'],
    'tipo_garantia': ['Ninguna', 'Vehiculo', 'Inmueble']
}

@app.route('/')
def index():
    """Página principal con el formulario de predicción"""
    return render_template('index.html', 
                         opciones=OPCIONES_CATEGORICAS,
                         modelo_nombre=modelo_nombre)

@app.route('/predecir', methods=['POST'])
def predecir():
    """Endpoint para realizar predicciones"""
    try:
        if modelo is None:
            return jsonify({
                'error': 'El modelo no está cargado. Por favor, entrena el modelo primero.'
            }), 500
        
        # Obtener datos del formulario
        datos = request.get_json()
        
        # Validar que todos los campos requeridos estén presentes
        campos_requeridos = [
            'edad', 'genero', 'zona', 'tipo_empleo', 'antiguedad', 'ingresos',
            'score_crediticio', 'pagos_previos', 'creditos_previos', 'monto_credito',
            'plazo_meses', 'destino_credito', 'tipo_garantia', 'valor_garantia',
            'precio_soya', 'precio_vino', 'uso_productos'
        ]
        
        campos_faltantes = [campo for campo in campos_requeridos if campo not in datos]
        if campos_faltantes:
            return jsonify({
                'error': f'Campos faltantes: {", ".join(campos_faltantes)}'
            }), 400
        
        # Crear DataFrame con los datos
        df_input = pd.DataFrame([datos])
        
        # Convertir tipos de datos numéricos
        columnas_numericas = [
            'edad', 'antiguedad', 'ingresos', 'score_crediticio', 
            'pagos_previos', 'creditos_previos', 'monto_credito', 
            'plazo_meses', 'valor_garantia', 'precio_soya', 
            'precio_vino', 'uso_productos'
        ]
        
        for col in columnas_numericas:
            df_input[col] = pd.to_numeric(df_input[col], errors='coerce')
        
        # Verificar valores nulos después de la conversión
        if df_input.isnull().any().any():
            columnas_con_nulos = df_input.columns[df_input.isnull().any()].tolist()
            return jsonify({
                'error': f'Valores inválidos en: {", ".join(columnas_con_nulos)}'
            }), 400
        
        # Realizar predicción
        prediccion = modelo.predict(df_input)[0]
        probabilidad = modelo.predict_proba(df_input)[0]
        
        # Preparar respuesta
        resultado = {
            'prediccion': int(prediccion),
            'prediccion_texto': 'MOROSO' if prediccion == 1 else 'NO MOROSO',
            'probabilidad_no_moroso': float(probabilidad[0]),
            'probabilidad_moroso': float(probabilidad[1]),
            'riesgo': clasificar_riesgo(probabilidad[1]),
            'recomendacion': generar_recomendacion(prediccion, probabilidad[1]),
            'datos_ingresados': datos,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Guardar predicción en log
        guardar_prediccion_log(resultado)
        
        return jsonify(resultado)
    
    except Exception as e:
        print(f"Error en predicción: {str(e)}")
        return jsonify({
            'error': f'Error al procesar la predicción: {str(e)}'
        }), 500

def clasificar_riesgo(probabilidad_moroso):
    """Clasifica el riesgo basado en la probabilidad de morosidad"""
    if probabilidad_moroso < 0.2:
        return 'BAJO'
    elif probabilidad_moroso < 0.5:
        return 'MEDIO'
    elif probabilidad_moroso < 0.7:
        return 'ALTO'
    else:
        return 'MUY ALTO'

def generar_recomendacion(prediccion, probabilidad_moroso):
    """Genera recomendaciones basadas en la predicción"""
    if prediccion == 0:
        if probabilidad_moroso < 0.1:
            return "Cliente de bajo riesgo. Se recomienda aprobar el crédito sin restricciones especiales."
        elif probabilidad_moroso < 0.3:
            return "Cliente de riesgo bajo-medio. Se recomienda aprobar con condiciones estándar."
        else:
            return "Cliente aprobable pero con atención. Considere solicitar garantías adicionales."
    else:
        if probabilidad_moroso > 0.7:
            return "Alto riesgo de morosidad. Se recomienda rechazar el crédito o solicitar garantías sólidas."
        elif probabilidad_moroso > 0.5:
            return "Riesgo medio-alto. Se recomienda evaluación adicional y garantías fuertes."
        else:
            return "Riesgo moderado. Considere aprobar con límites reducidos y seguimiento cercano."

def guardar_prediccion_log(resultado):
    """Guarda las predicciones en un archivo de log"""
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, f'predicciones_{datetime.now().strftime("%Y%m%d")}.json')
    
    try:
        # Leer predicciones existentes
        if os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                predicciones = json.load(f)
        else:
            predicciones = []
        
        # Añadir nueva predicción
        predicciones.append(resultado)
        
        # Guardar
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(predicciones, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar log: {e}")

@app.route('/estadisticas')
def estadisticas():
    """Página con estadísticas de predicciones"""
    return render_template('estadisticas.html', modelo_nombre=modelo_nombre)

@app.route('/api/estadisticas')
def api_estadisticas():
    """API para obtener estadísticas de las predicciones realizadas"""
    try:
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            return jsonify({'total': 0, 'morosos': 0, 'no_morosos': 0})
        
        # Leer todas las predicciones del día
        log_file = os.path.join(log_dir, f'predicciones_{datetime.now().strftime("%Y%m%d")}.json')
        
        if not os.path.exists(log_file):
            return jsonify({'total': 0, 'morosos': 0, 'no_morosos': 0})
        
        with open(log_file, 'r', encoding='utf-8') as f:
            predicciones = json.load(f)
        
        total = len(predicciones)
        morosos = sum(1 for p in predicciones if p['prediccion'] == 1)
        no_morosos = total - morosos
        
        # Calcular promedios de probabilidad
        if total > 0:
            prob_moroso_promedio = np.mean([p['probabilidad_moroso'] for p in predicciones])
        else:
            prob_moroso_promedio = 0
        
        return jsonify({
            'total': total,
            'morosos': morosos,
            'no_morosos': no_morosos,
            'prob_moroso_promedio': float(prob_moroso_promedio),
            'ultima_prediccion': predicciones[-1]['timestamp'] if predicciones else None
        })
    
    except Exception as e:
        print(f"Error al obtener estadísticas: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    """Página con información del modelo"""
    return render_template('about.html', modelo_nombre=modelo_nombre)

@app.route('/demo')
def demo():
    """Página de demostración con perfiles pre-cargados"""
    return render_template('demo.html', modelo_nombre=modelo_nombre)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("SISTEMA DE PREDICCIÓN DE MOROSIDAD - AHORRO VALLE")
    print("="*70)
    print(f"Modelo cargado: {modelo_nombre}")
    print("Servidor iniciando en: http://127.0.0.1:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
