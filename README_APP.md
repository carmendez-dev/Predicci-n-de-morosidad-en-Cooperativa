# Sistema de Predicción de Morosidad - Ahorro Valle Sistema web interactivo para predecir la probabilidad de morosidad crediticia utilizando Machine Learning. ## Descripción Este sistema permite a los analistas de crédito de Ahorro Valle evaluar automáticamente el riesgo de morosidad de los solicitantes de préstamos mediante un modelo de Machine Learning entrenado con datos históricos. ## Características - Predicción de morosidad en tiempo real
- Visualización de probabilidades y nivel de riesgo
- Recomendaciones automáticas basadas en el resultado
- Panel de estadísticas de predicciones realizadas
- Interfaz web moderna y responsiva
- Registro de predicciones en logs
- Función de impresión de resultados ## Requisitos - Python 3.8 o superior
- Navegador web moderno (Chrome, Firefox, Edge) ### Dependencias de Python ```
Flask==3.1.0
flask-cors==5.0.1
joblib==1.5.2
pandas==2.3.3
numpy==2.3.4
scikit-learn==1.7.2
``` ## Instalación 1. **Instalar dependencias:** ```bash
pip install Flask flask-cors joblib pandas numpy scikit-learn
``` O usando el archivo requirements.txt: ```bash
pip install -r requirements.txt
``` 2. **Verificar que existe el modelo entrenado:** Asegúrate de que existe al menos un archivo `.joblib` en el directorio `output/` con el nombre que comienza con `model_pipeline_final_`. ## Ejecución ### Iniciar el servidor ```bash
python app.py
``` El servidor se iniciará en: **http://127.0.0.1:5000** También será accesible desde otras computadoras en la red local usando tu IP. ### Acceder a la aplicación Abre tu navegador y visita:
- Predicción: http://127.0.0.1:5000/
- Estadísticas: http://127.0.0.1:5000/estadisticas
- Información: http://127.0.0.1:5000/about ## Uso del Sistema ### 1. Realizar una Predicción 1. Accede a la página principal
2. Completa el formulario con los datos del solicitante: - **Datos Personales:** edad, género, zona de residencia - **Información Laboral:** tipo de empleo, antigüedad, ingresos - **Historial Crediticio:** score, pagos previos, créditos previos - **Crédito Solicitado:** monto, plazo, destino - **Garantías:** tipo y valor de la garantía - **Variables Económicas:** precios de soya y vino, uso de productos
3. Haz clic en "Predecir Morosidad"
4. Revisa el resultado que incluye: - Predicción (Moroso / No Moroso) - Probabilidades - Nivel de riesgo (Bajo, Medio, Alto, Muy Alto) - Recomendación para la aprobación del crédito ### 2. Ver Estadísticas - Accede a la sección "Estadísticas" para ver: - Total de predicciones realizadas en el día - Distribución de morosos vs no morosos - Riesgo promedio - Última predicción realizada ### 3. Consultar Información del Modelo - En la sección "Acerca de" encontrarás: - Descripción del sistema - Información del modelo de ML - Variables consideradas - Proceso de predicción - Clasificación de riesgo - Consideraciones importantes ## Interpretación de Resultados ### Niveles de Riesgo | Nivel | Probabilidad de Morosidad | Descripción |
|-------|---------------------------|-------------|
| **BAJO** | < 20% | Cliente confiable, bajo riesgo |
| **MEDIO** | 20% - 50% | Riesgo moderado, requiere evaluación |
| **ALTO** | 50% - 70% | Alto riesgo, considerar garantías adicionales |
| **MUY ALTO** | > 70% | Riesgo muy elevado, posible rechazo | ### Recomendaciones El sistema genera automáticamente recomendaciones basadas en:
- La predicción (Moroso / No Moroso)
- La probabilidad de morosidad
- El nivel de riesgo calculado ## Estructura del Proyecto ```
AhorroValle/ app.py # Aplicación Flask principal morosidadTrain.py # Script de entrenamiento del modelo requirements.txt # Dependencias de Python dataset_credito_morosidad.csv # Dataset de entrenamiento templates/ # Plantillas HTML index.html # Página principal (predicción) estadisticas.html # Página de estadísticas about.html # Página de información static/ # Archivos estáticos css/ style.css # Estilos CSS js/ main.js # JavaScript principal estadisticas.js # JavaScript de estadísticas output/ # Modelos y resultados entrenados model_pipeline_final_*.joblib training_results_*.json plot_*.png logs/ # Logs de predicciones predicciones_*.json
``` ## Seguridad y Consideraciones ### Importante **Este sistema es una herramienta de apoyo a la decisión**, no debe ser el único criterio para aprobar o rechazar créditos. ### Recomendaciones de Uso 1. Utilizar el sistema como complemento al análisis humano
2. Considerar factores adicionales no incluidos en el modelo
3. Realizar evaluaciones adicionales para créditos de alto monto
4. Revisar y actualizar el modelo periódicamente
5. Mantener logs de todas las predicciones para auditoría ### Privacidad de Datos - Los datos ingresados se almacenan solo en logs locales
- No se envían datos a servidores externos
- Los logs se pueden eliminar manualmente del directorio `logs/` ## Mantenimiento ### Actualizar el Modelo Para usar un nuevo modelo entrenado: 1. Entrena un nuevo modelo ejecutando: ```bash python morosidadTrain.py ``` 2. El nuevo modelo se guardará automáticamente en `output/` 3. Reinicia la aplicación Flask: - Detén el servidor (Ctrl+C) - Vuelve a ejecutar `python app.py` 4. La aplicación cargará automáticamente el modelo más reciente ### Revisar Logs Los logs de predicciones se guardan en:
```
logs/predicciones_YYYYMMDD.json
``` Cada archivo contiene todas las predicciones realizadas en ese día. ## Solución de Problemas ### Error: "No se encontró ningún modelo entrenado" **Solución:** Ejecuta primero el script de entrenamiento:
```bash
python morosidadTrain.py
``` ### Error: "Module not found" **Solución:** Instala las dependencias faltantes:
```bash
pip install -r requirements.txt
``` ### El servidor no inicia **Solución:** Verifica que el puerto 5000 no esté en uso:
- Windows: `netstat -ano | findstr :5000`
- Linux/Mac: `lsof -i :5000` ### La página no carga **Solución:** 1. Verifica que el servidor esté corriendo
2. Revisa la consola por errores
3. Prueba acceder a http://127.0.0.1:5000 directamente ## Soporte Para problemas técnicos o preguntas:
- Revisa los logs del servidor en la consola
- Verifica el archivo de logs en `logs/`
- Consulta la documentación del código ## Licencia Sistema desarrollado para uso académico - EC2 Modelado y Simulación de Sistemas. ## Créditos - **Sistema:** Predicción de Morosidad - Ahorro Valle
- **Modelo:** Regresión Logística Optimizada
- **Framework:** Flask + Scikit-learn
- **Año:** 2025 --- **¡Gracias por usar el Sistema de Predicción de Morosidad!**
