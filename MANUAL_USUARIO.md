# Manual de Usuario
## Sistema de Predicción de Morosidad - Ahorro Valle

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [Acceso al Sistema](#acceso-al-sistema)
3. [Realizar una Predicción](#realizar-una-predicción)
4. [Interpretar Resultados](#interpretar-resultados)
5. [Dashboard de Estadísticas](#dashboard-de-estadísticas)
6. [Modo Demo](#modo-demo)
7. [Casos de Uso Comunes](#casos-de-uso-comunes)
8. [Solución de Problemas](#solución-de-problemas)
9. [Soporte y Contacto](#soporte-y-contacto)

---

## Introducción

### ¿Qué es el Sistema de Predicción de Morosidad?

El **Sistema de Predicción de Morosidad de Ahorro Valle** es una herramienta inteligente que ayuda a los analistas de crédito a evaluar el riesgo de que un solicitante no pague su crédito. Utiliza **Machine Learning** para analizar múltiples factores y proporcionar una recomendación informada.

### ¿Para quién está diseñado?

- **Analistas de Crédito**
- **Gerentes de Sucursal**  
- **Supervisores de Riesgo**
- **Personal Autorizado de Ahorro Valle**

### Beneficios Principales

- **Evaluación Objetiva**: Reduce sesgos en decisiones crediticias
- **Ahorro de Tiempo**: Análisis automático en segundos
- **Mejor Gestión de Riesgo**: Identificación temprana de riesgos
- **Documentación Completa**: Registro de todas las evaluaciones
- **Interfaz Intuitiva**: Fácil de usar sin conocimientos técnicos

---

## Acceso al Sistema

### Requisitos del Sistema

**Navegador Compatible:**
- Google Chrome (Recomendado)
- Mozilla Firefox
- Microsoft Edge
- Safari

**Conexión a Internet:**
- Requerida para acceso al sistema
- Velocidad mínima recomendada: 1 Mbps

### Cómo Acceder

1. **Abrir navegador web**
2. **Ingresar la dirección:** `http://127.0.0.1:5000`
3. **Verificar que aparezca la página principal**

### Navegación Principal

La interfaz principal contiene las siguientes secciones:

- **Predicción**: Evaluación de nuevos solicitantes
- **Estadísticas**: Dashboard con métricas del día
- **Demo**: Ejemplos y casos de prueba
- **Acerca de**: Información del sistema

---

## Realizar una Predicción

### Paso 1: Acceder al Formulario

1. Clic en **"Predicción"** en el menú principal
2. Se abrirá el formulario de evaluación crediticia

### Paso 2: Completar Datos del Solicitante

El formulario está organizado en **6 secciones**:

#### **1. DATOS PERSONALES**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Edad** | Edad del solicitante (18-80 años) | `35` |
| **Género** | Seleccionar de la lista | `Masculino/Femenino` |
| **Zona de Residencia** | Ubicación geográfica | `Urbana/Rural` |

#### **2. INFORMACIÓN LABORAL**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Tipo de Empleo** | Situación laboral actual | `Empleado/Independiente` |
| **Antigüedad Laboral** | Años en el trabajo actual | `5` |
| **Ingresos Mensuales** | Ingresos en pesos colombianos | `3000000` |

#### **3. DETALLES DEL CRÉDITO**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Monto del Crédito** | Cantidad solicitada (COP) | `15000000` |
| **Plazo en Meses** | Duración del crédito | `24` |
| **Destino del Crédito** | Uso del dinero | `Vivienda/Personal/Vehículo` |

#### **4. GARANTÍAS**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Tipo de Garantía** | Respaldo del crédito | `Hipotecaria/Prendaria/Sin garantía` |
| **Valor de la Garantía** | Valor en pesos (COP) | `25000000` |

#### **5. HISTORIAL CREDITICIO**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Credit Score** | Puntaje crediticio (300-850) | `650` |
| **Pagos Anteriores** | Número de pagos realizados | `12` |
| **Créditos Anteriores** | Cantidad de créditos previos | `3` |

#### **6. VARIABLES ECONÓMICAS**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Precio Soya** | Precio actual del commodity | `1500` |
| **Precio Vino** | Precio actual del producto | `8000` |
| **Uso Productos Financieros** | Cantidad de productos usados | `2` |

### Paso 3: Validación Automática

El sistema valida automáticamente:

- **Campos Obligatorios**: Todos los campos requeridos completados
- **Rangos Válidos**: Valores dentro de límites aceptables
- **Tipos de Datos**: Números donde corresponde
- **Lógica de Negocio**: Coherencia entre datos

### Paso 4: Enviar Predicción

1. **Verificar** que todos los campos estén completados
2. **Clic en "Predecir Morosidad"**
3. **Esperar** el resultado (generalmente 1-2 segundos)

---

## Interpretar Resultados

### Tipos de Resultado

El sistema proporciona los siguientes elementos:

#### **1. Predicción Principal**
```
RESULTADO: NO MOROSO
```
- **NO MOROSO**: Baja probabilidad de incumplimiento
- **MOROSO**: Alta probabilidad de incumplimiento

#### **2. Probabilidades Exactas**
```
Probabilidad de No Morosidad: 72.5%
Probabilidad de Morosidad: 27.5%
```

#### **3. Clasificación de Riesgo**

| Nivel de Riesgo | Probabilidad de Morosidad | Color | Acción Recomendada |
|-----------------|---------------------------|-------|-------------------|
| **BAJO** | < 30% | Verde | Aprobar con condiciones estándar |
| **MEDIO** | 30% - 60% | Amarillo | Revisar garantías adicionales |
| **ALTO** | 60% - 80% | Naranja | Evaluación manual requerida |
| **MUY ALTO** | > 80% | Rojo | Rechazar o reestructurar |

#### **4. Recomendación Automática**

Ejemplos de recomendaciones:
- **"APROBAR - Riesgo bajo, perfil crediticio favorable"**
- **"REVISAR - Considerar garantías adicionales"**
- **"RECHAZAR - Alto riesgo de incumplimiento"**
- **"REESTRUCTURAR - Reducir monto o aumentar plazo"**

### Ejemplo de Resultado Completo

```
===============================================
RESULTADO DE PREDICCIÓN DE MOROSIDAD
===============================================

PREDICCIÓN: NO MOROSO
Probabilidad de No Morosidad: 72.5%
Probabilidad de Morosidad: 27.5%

CLASIFICACIÓN DE RIESGO: BAJO
Nivel de confianza: Alto

RECOMENDACIÓN: APROBAR
Riesgo bajo, perfil crediticio favorable.
Considerar condiciones estándar.

FACTORES PRINCIPALES:
✓ Credit Score alto (720)
✓ Ingresos estables y suficientes
✓ Historial crediticio positivo
⚠ Monto de crédito significativo

FECHA: 2025-01-28 14:30:25
===============================================
```

---

## Dashboard de Estadísticas

### Acceso al Dashboard

1. Clic en **"Estadísticas"** en el menú principal
2. Se mostrará el panel de métricas en tiempo real

### Métricas Disponibles

#### **Estadísticas del Día**
- Total de predicciones realizadas
- Porcentaje de aprobaciones
- Porcentaje de rechazos
- Tiempo promedio de procesamiento

#### **Distribución de Riesgo**
Gráfico circular mostrando:
- Riesgo Bajo (%)
- Riesgo Medio (%)
- Riesgo Alto (%)
- Riesgo Muy Alto (%)

#### **Tendencias por Hora**
Gráfico de líneas mostrando la actividad del sistema a lo largo del día.

#### **Top 5 Factores de Riesgo**
Lista de las variables que más influyen en las predicciones del día.

---

## Modo Demo

### ¿Qué es el Modo Demo?

El modo demo permite probar el sistema con casos predefinidos sin afectar las estadísticas reales.

### Cómo Usar el Demo

1. **Clic en "Demo"** en el menú principal
2. **Seleccionar un caso** de la lista disponible:
   - Cliente de Bajo Riesgo
   - Cliente de Riesgo Medio
   - Cliente de Alto Riesgo
   - Cliente de Muy Alto Riesgo
3. **Ver resultado** automáticamente cargado

### Casos Demo Disponibles

#### **Caso 1: Bajo Riesgo**
- Empleado de 35 años
- Ingresos altos y estables
- Buen historial crediticio
- **Resultado esperado**: APROBAR

#### **Caso 2: Riesgo Medio**
- Independiente de 28 años
- Ingresos variables
- Historial crediticio limitado
- **Resultado esperado**: REVISAR

#### **Caso 3: Alto Riesgo**
- Empleado de 55 años
- Ingresos justos
- Múltiples créditos anteriores
- **Resultado esperado**: EVALUACIÓN MANUAL

#### **Caso 4: Muy Alto Riesgo**
- Independiente de 22 años
- Ingresos bajos e inestables
- Sin historial crediticio
- **Resultado esperado**: RECHAZAR

---

## Casos de Uso Comunes

### 1. Evaluación Rutinaria de Solicitudes

**Proceso:**
1. Recibir solicitud de crédito del cliente
2. Ingresar datos al sistema
3. Obtener recomendación automática
4. Complementar con análisis manual
5. Tomar decisión final

**Tiempo estimado:** 3-5 minutos por solicitud

### 2. Análisis de Cartera Existente

**Proceso:**
1. Seleccionar clientes de la cartera actual
2. Re-evaluar con datos actualizados
3. Identificar clientes de alto riesgo
4. Implementar medidas preventivas

**Beneficio:** Gestión proactiva del riesgo

### 3. Capacitación de Personal Nuevo

**Proceso:**
1. Usar modo demo con diferentes casos
2. Explicar criterios de evaluación
3. Comparar resultados automáticos vs manuales
4. Desarrollar criterios de juicio

**Duración:** 2-3 horas de entrenamiento

### 4. Validación de Políticas de Crédito

**Proceso:**
1. Procesar solicitudes históricas
2. Comparar recomendaciones con decisiones tomadas
3. Identificar patrones y discrepancias
4. Ajustar políticas según sea necesario

---

## Solución de Problemas

### Problemas Comunes

#### **Error: "Campos requeridos faltantes"**
**Causa:** No se completaron todos los campos obligatorios
**Solución:** Verificar que todos los campos tengan valores válidos

#### **Error: "Valor fuera de rango"**
**Causa:** Se ingresó un valor fuera de los límites permitidos
**Solución:** Verificar los rangos válidos para cada campo

#### **Error: "Sistema temporalmente no disponible"**
**Causa:** Sobrecarga del sistema o mantenimiento
**Solución:** Esperar unos minutos e intentar nuevamente

#### **La página no carga**
**Causa:** Problema de conexión o dirección incorrecta
**Solución:** 
1. Verificar conexión a internet
2. Confirmar la dirección: `http://127.0.0.1:5000`
3. Refrescar la página (Ctrl+F5)

#### **Predicción toma mucho tiempo**
**Causa:** Alta carga del sistema
**Solución:** 
1. Esperar hasta 30 segundos
2. Si no responde, refrescar página
3. Intentar en horario de menor actividad

### Mensajes de Error Específicos

#### **E001: Campos faltantes**
```
Error: Campos requeridos faltantes
Campos: edad, ingresos_mensuales
Acción: Completar los campos indicados
```

#### **E002: Tipo de dato incorrecto**
```
Error: Tipo de dato incorrecto
Campo: edad
Esperado: número
Recibido: texto
Acción: Ingresar solo números
```

#### **E003: Valor fuera de rango**
```
Error: Valor fuera de rango
Campo: edad  
Valor: 150
Rango válido: 18-80
Acción: Ingresar edad válida
```

### Mejores Prácticas

1. **Verificar datos** antes de enviar predicción
2. **Usar valores realistas** en todos los campos
3. **Interpretar resultados** junto con análisis manual
4. **Documentar decisiones** tomadas
5. **Actualizar datos** económicos periódicamente

---

## Soporte y Contacto

### Obtener Ayuda

#### **Soporte Técnico**
- **Email**: soporte@ahorrovalle.com
- **Teléfono**: +57 300 123 4567
- **Horario**: Lunes a Viernes, 8:00 AM - 6:00 PM

#### **Capacitación**
- **Email**: capacitacion@ahorrovalle.com
- **Solicitar**: Sesiones de entrenamiento personalizadas
- **Duración**: 2-4 horas según necesidades

#### **Reportar Problemas**
- **Email**: bugs@ahorrovalle.com
- **Incluir**: 
  - Descripción detallada del problema
  - Pasos para reproducir el error
  - Captura de pantalla si es posible
  - Navegador y sistema operativo usado

### Información de Contacto

#### **Equipo de Desarrollo**
- **Carmen Mendez** - Desarrolladora Principal
- **Email**: carmen.mendez@ucb.edu.bo
- **Universidad**: Universidad Católica Boliviana "San Pablo"

#### **Retroalimentación**
Sus comentarios y sugerencias son importantes para mejorar el sistema:
- **Email**: feedback@ahorrovalle.com
- **Incluir**: Sugerencias de mejora, casos de uso adicionales, problemas de usabilidad

---

## Recursos Adicionales

### Documentación Técnica
- [Documentación Técnica Completa](DOCUMENTACION_TECNICA.md)
- [Guía de Instalación](GUIA_RAPIDA.md)
- [Manejo de Errores](MANEJO_ERRORES.md)

### Videos Tutoriales
*(Próximamente disponibles)*
- Tutorial básico de uso (5 min)
- Interpretación de resultados (10 min)
- Casos de uso avanzados (15 min)

### Actualizaciones
- **Versión actual**: 1.0
- **Última actualización**: 28 de Octubre, 2025
- **Próxima actualización**: Diciembre 2025

---

**© 2025 Sistema de Predicción de Morosidad - Ahorro Valle**  
**Desarrollado por Carmen Mendez - Universidad Católica Boliviana "San Pablo"**  
**Manual de Usuario - Versión 1.0**