"""
Script de ejemplo para probar la API de predicción de morosidad
"""
import requests
import json

# URL de la API
API_URL = "http://127.0.0.1:5000/predecir"

# Datos de ejemplo para un cliente
datos_cliente_1 = {
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

# Cliente con perfil de alto riesgo
datos_cliente_2 = {
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

# Cliente con perfil de bajo riesgo
datos_cliente_3 = {
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

def probar_prediccion(datos, nombre_cliente):
    """Realiza una predicción y muestra los resultados"""
    print(f"\n{'='*70}")
    print(f"PREDICCIÓN PARA: {nombre_cliente}")
    print(f"{'='*70}")
    
    try:
        # Enviar petición POST
        response = requests.post(API_URL, json=datos)
        
        if response.status_code == 200:
            resultado = response.json()
            
            # Mostrar resultados
            print(f"\n PREDICCIÓN: {resultado['prediccion_texto']}")
            print(f"   Probabilidad de NO Morosidad: {resultado['probabilidad_no_moroso']*100:.2f}%")
            print(f"   Probabilidad de Morosidad: {resultado['probabilidad_moroso']*100:.2f}%")
            print(f"   Nivel de Riesgo: {resultado['riesgo']}")
            print(f"\n RECOMENDACIÓN:")
            print(f"   {resultado['recomendacion']}")
            print(f"\n📅 Timestamp: {resultado['timestamp']}")
            
        else:
            print(f" Error: {response.status_code}")
            print(f"   {response.json().get('error', 'Error desconocido')}")
            
    except requests.exceptions.ConnectionError:
        print(" Error: No se puede conectar al servidor.")
        print("   Asegúrate de que el servidor Flask esté corriendo.")
    except Exception as e:
        print(f" Error inesperado: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" PRUEBAS DE LA API DE PREDICCIÓN DE MOROSIDAD")
    print("="*70)
    
    # Probar con diferentes perfiles
    probar_prediccion(datos_cliente_1, "Cliente 1 - Perfil Moderado")
    probar_prediccion(datos_cliente_2, "Cliente 2 - Alto Riesgo")
    probar_prediccion(datos_cliente_3, "Cliente 3 - Bajo Riesgo")
    
    print("\n" + "="*70)
    print(" PRUEBAS COMPLETADAS")
    print("="*70 + "\n")
