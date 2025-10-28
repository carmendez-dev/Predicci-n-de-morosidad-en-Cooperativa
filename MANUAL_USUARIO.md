# 👥 MANUAL DE USUARIO
## Sistema de Predicción de Morosidad - Ahorro Valle

---

## 📋 ÍNDICE

1. [🎯 Introducción](#-introducción)
2. [🚀 Acceso al Sistema](#-acceso-al-sistema)
3. [📝 Realizar una Predicción](#-realizar-una-predicción)
4. [📊 Interpretar Resultados](#-interpretar-resultados)
5. [📈 Dashboard de Estadísticas](#-dashboard-de-estadísticas)
6. [🎮 Modo Demo](#-modo-demo)
7. [💡 Casos de Uso Comunes](#-casos-de-uso-comunes)
8. [⚠️ Solución de Problemas](#️-solución-de-problemas)
9. [📞 Soporte y Contacto](#-soporte-y-contacto)

---

## 🎯 INTRODUCCIÓN

### ¿Qué es el Sistema de Predicción de Morosidad?

El **Sistema de Predicción de Morosidad de Ahorro Valle** es una herramienta inteligente que ayuda a los analistas de crédito a evaluar el riesgo de que un solicitante no pague su crédito. Utiliza **Machine Learning** para analizar múltiples factores y proporcionar una recomendación informada.

### ¿Para quién está diseñado?

- 👤 **Analistas de Crédito**
- 👔 **Gerentes de Sucursal**
- 📊 **Supervisores de Riesgo**
- 🏦 **Personal Autorizado de Ahorro Valle**

### Beneficios principales:

✅ **Evaluación Objetiva**: Reduce sesgos en decisiones crediticias
✅ **Ahorro de Tiempo**: Análisis automático en segundos
✅ **Mejor Gestión de Riesgo**: Identificación temprana de riesgos
✅ **Documentación Completa**: Registro de todas las evaluaciones
✅ **Interfaz Intuitiva**: Fácil de usar sin conocimientos técnicos

---

## 🚀 ACCESO AL SISTEMA

### Requisitos del Sistema

**Navegador Compatible:**
- ✅ Google Chrome (Recomendado)
- ✅ Mozilla Firefox
- ✅ Microsoft Edge
- ✅ Safari

**Conexión a Internet:**
- Requerida para acceso al sistema
- Velocidad mínima recomendada: 1 Mbps

### Acceder al Sistema

1. **Abrir navegador web**
2. **Ingresar la dirección:** `http://127.0.0.1:5000`
3. **Verificar que aparezca la página principal**

### Navegación Principal

```
┌─────────────────────────────────────────────┐
│  🏦 Sistema de Predicción de Morosidad      │
│     Ahorro Valle - Modelo Activo           │
└─────────────────────────────────────────────┘
│                                             │
│ [📝 Predicción] [📊 Estadísticas]          │
│ [🎮 Demo]       [ℹ️ Acerca de]             │
│                                             │
└─────────────────────────────────────────────┘
```

**Secciones disponibles:**
- **📝 Predicción**: Evaluación de nuevos solicitantes
- **📊 Estadísticas**: Dashboard con métricas del día
- **🎮 Demo**: Ejemplos y casos de prueba
- **ℹ️ Acerca de**: Información del sistema

---

## 📝 REALIZAR UNA PREDICCIÓN

### Paso 1: Acceder al Formulario

1. Clic en **"📝 Predicción"** en el menú principal
2. Se abrirá el formulario de evaluación crediticia

### Paso 2: Completar Datos del Solicitante

El formulario está organizado en **6 secciones**:

#### 👤 **DATOS PERSONALES**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Edad** | Edad del solicitante (18-80 años) | `35` |
| **Género** | Seleccionar de la lista | `Masculino/Femenino` |
| **Zona de Residencia** | Ubicación geográfica | `Urbana/Rural` |

#### 💼 **INFORMACIÓN LABORAL**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Tipo de Empleo** | Situación laboral actual | `Empleado/Independiente` |
| **Antigüedad Laboral** | Años en el trabajo actual | `5` |
| **Ingresos Mensuales** | Ingresos en pesos colombianos | `3000000` |

#### 💰 **DETALLES DEL CRÉDITO**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Monto del Crédito** | Cantidad solicitada (COP) | `15000000` |
| **Plazo en Meses** | Duración del crédito | `24` |
| **Destino del Crédito** | Uso del dinero | `Vivienda/Personal/Vehículo` |

#### 🏠 **GARANTÍAS**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Tipo de Garantía** | Respaldo del crédito | `Hipotecaria/Prendaria/Sin garantía` |
| **Valor de la Garantía** | Valor en pesos (COP) | `25000000` |

#### 📊 **HISTORIAL CREDITICIO**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Credit Score** | Puntaje crediticio (300-850) | `650` |
| **Pagos Anteriores** | Número de pagos realizados | `12` |
| **Créditos Anteriores** | Cantidad de créditos previos | `3` |

#### 📈 **VARIABLES ECONÓMICAS**

| Campo | Descripción | Ejemplo |
|-------|-------------|---------|
| **Precio Soya** | Precio actual del commodity | `1500` |
| **Precio Vino** | Precio actual del producto | `8000` |
| **Uso Productos Financieros** | Cantidad de productos usados | `2` |

### Paso 3: Validación Automática

El sistema valida automáticamente:

✅ **Campos Obligatorios**: Todos los campos requeridos completados
✅ **Rangos Válidos**: Valores dentro de límites aceptables
✅ **Tipos de Datos**: Números donde corresponde
✅ **Lógica de Negocio**: Coherencia entre datos

**Ejemplo de validación:**
```
⚠️ Advertencias mostradas en tiempo real:
• "El monto solicitado es alto comparado con los ingresos"
• "Edad debe estar entre 18 y 80 años"
• "Ingresos deben ser un número positivo"
```

### Paso 4: Realizar Predicción

1. **Revisar todos los datos ingresados**
2. **Clic en el botón "🔍 Predecir"**
3. **Esperar resultado (2-3 segundos)**

---

## 📊 INTERPRETAR RESULTADOS

### Resultado de la Predicción

Una vez procesada, el sistema muestra:

```
┌─────────────────────────────────────────────┐
│  📋 EVALUACIÓN: NO MOROSO 🟢               │
│                                             │
│  Probabilidad No Moroso: ████████████ 72.3%│
│  Probabilidad Moroso:    ███░░░░░░░░░ 27.7% │
│                                             │
│  Nivel de Riesgo: MEDIO 🟡                 │
│                                             │
│  💡 Recomendación:                          │
│  Cliente de riesgo bajo-medio. Se           │
│  recomienda aprobar con condiciones         │
│  estándar de la entidad.                    │
│                                             │
│  📅 2025-10-28 14:30:15                    │
│                                             │
│  [➕ Nueva Evaluación] [🖨️ Imprimir]      │
└─────────────────────────────────────────────┘
```

### Componentes del Resultado

#### 1. **Predicción Principal**
- **🟢 NO MOROSO**: Cliente probablemente pagará
- **🔴 MOROSO**: Cliente probablemente no pagará

#### 2. **Probabilidades**
- **Barra visual** que muestra la confianza del modelo
- **Porcentajes exactos** para documentación
- **Suma siempre 100%**

#### 3. **Clasificación de Riesgo**
- **🟢 BAJO**: Riesgo menor al 30%
- **🟡 MEDIO**: Riesgo entre 30% y 60%
- **🔴 ALTO**: Riesgo mayor al 60%

#### 4. **Recomendación Automática**
El sistema sugiere acciones específicas:

**Para Riesgo Bajo:**
```
✅ "Cliente de bajo riesgo. Se recomienda aprobar 
   con condiciones preferenciales."
```

**Para Riesgo Medio:**
```
⚠️ "Cliente de riesgo medio. Se recomienda aprobar 
   con condiciones estándar y seguimiento."
```

**Para Riesgo Alto:**
```
❌ "Cliente de alto riesgo. Se recomienda rechazar 
   o solicitar garantías adicionales."
```

### Interpretación Práctica

#### Ejemplo 1: Cliente Aprobable
```
Predicción: NO MOROSO (85% confianza)
Riesgo: BAJO
Decisión Sugerida: ✅ APROBAR
Condiciones: Tasa preferencial, plazo normal
```

#### Ejemplo 2: Cliente Requiere Análisis
```
Predicción: NO MOROSO (55% confianza)
Riesgo: MEDIO
Decisión Sugerida: ⚠️ APROBAR CON CONDICIONES
Condiciones: Tasa estándar, garantías adicionales
```

#### Ejemplo 3: Cliente Alto Riesgo
```
Predicción: MOROSO (75% confianza)
Riesgo: ALTO
Decisión Sugerida: ❌ RECHAZAR O EVALUAR
Condiciones: Garantías sustanciales, análisis adicional
```

---

## 📈 DASHBOARD DE ESTADÍSTICAS

### Acceder al Dashboard

1. **Clic en "📊 Estadísticas"** en el menú principal
2. **Se carga automáticamente** el dashboard del día actual

### Métricas Principales

```
┌─────────────────────────────────────────────┐
│           📊 ESTADÍSTICAS DEL DÍA           │
│                                             │
│ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌──────┐│
│ │   📝    │ │   ✅    │ │   ⚠️    │ │  📊 ││
│ │   25    │ │   18    │ │    7    │ │23.4%││
│ │ Total   │ │   No    │ │ Morosos │ │Riesgo││
│ │Predict. │ │ Morosos │ │         │ │Prom. ││
│ └─────────┘ └─────────┘ └─────────┘ └──────┘│
└─────────────────────────────────────────────┘
```

#### Interpretación de Métricas:

**📝 Total Predicciones:**
- Cantidad de evaluaciones realizadas en el día
- Incluye todas las consultas procesadas

**✅ No Morosos:**
- Clientes evaluados como "pagadores"
- Porcentaje de aprobaciones del día

**⚠️ Morosos:**
- Clientes evaluados como "riesgo alto"
- Ayuda a monitorear tendencias de riesgo

**📊 Riesgo Promedio:**
- Promedio de probabilidad de morosidad
- Indicador de la calidad general de solicitudes

### Gráfico de Distribución

```
DISTRIBUCIÓN DE PREDICCIONES
┌─────────────────────────────────────────────┐
│                                             │
│ No Morosos (72%) ████████████████████████   │
│                                             │
│ Morosos (28%)    ████████░░░░░░░░░░░░░░░░░   │
│                                             │
│        Total de Evaluaciones: 25           │
└─────────────────────────────────────────────┘
```

### Actualización Automática

- **Se actualiza cada 30 segundos**
- **Muestra datos en tiempo real**
- **Clic en "🔄 Actualizar" para refresh manual**

---

## 🎮 MODO DEMO

### ¿Qué es el Modo Demo?

Sección con **ejemplos predefinidos** para:
- 🎓 **Aprender a usar el sistema**
- 🧪 **Probar diferentes escenarios**
- 📚 **Capacitar nuevo personal**

### Perfiles de Ejemplo Disponibles

#### 1. **👤 Cliente Ideal**
```
Perfil: Empleado con buen historial
- Edad: 35 años
- Ingresos: $4,000,000
- Credit Score: 750
- Empleo estable: 5 años

Resultado Esperado: ✅ BAJO RIESGO
```

#### 2. **⚠️ Cliente Medio Riesgo**
```
Perfil: Independiente con historial mixto
- Edad: 45 años
- Ingresos: $2,500,000
- Credit Score: 620
- Empleo: 2 años

Resultado Esperado: 🟡 RIESGO MEDIO
```

#### 3. **🚨 Cliente Alto Riesgo**
```
Perfil: Joven sin historial
- Edad: 22 años
- Ingresos: $1,200,000
- Credit Score: 480
- Sin empleo fijo

Resultado Esperado: 🔴 ALTO RIESGO
```

### Cómo Usar el Demo

1. **Seleccionar un perfil** de la lista
2. **Los datos se cargan automáticamente**
3. **Clic en "🔍 Predecir"**
4. **Ver resultado y aprender**
5. **Modificar datos** para ver cómo cambia la predicción

---

## 💡 CASOS DE USO COMUNES

### Caso 1: Evaluación Rutinaria de Crédito

**Situación:** Cliente solicita crédito para compra de vivienda

**Proceso:**
1. ✅ Recopilar documentos del cliente
2. ✅ Ingresar datos en el sistema
3. ✅ Obtener predicción automática
4. ✅ Revisar recomendación
5. ✅ Tomar decisión informada

**Tiempo estimado:** 5-10 minutos

### Caso 2: Análisis de Cartera de Solicitantes

**Situación:** Evaluar múltiples solicitudes en un día

**Proceso:**
1. ✅ Procesar cada solicitud individualmente
2. ✅ Documentar resultados
3. ✅ Revisar estadísticas del día
4. ✅ Identificar patrones de riesgo
5. ✅ Generar reporte para gerencia

**Beneficio:** Consistencia en evaluaciones

### Caso 3: Capacitación de Personal

**Situación:** Entrenar nuevo analista de crédito

**Proceso:**
1. ✅ Usar modo Demo con ejemplos
2. ✅ Explicar interpretación de resultados
3. ✅ Practicar con casos reales
4. ✅ Comparar criterios tradicionales vs ML
5. ✅ Validar conocimientos adquiridos

**Duración sugerida:** 2-3 horas de práctica

### Caso 4: Revisión de Decisiones Borderline

**Situación:** Cliente con predicción de riesgo medio

**Proceso:**
1. ✅ Obtener predicción inicial
2. ✅ Revisar factores de riesgo específicos
3. ✅ Solicitar información adicional si necesario
4. ✅ Re-evaluar con datos actualizados
5. ✅ Tomar decisión final documentada

**Criterio:** Usar predicción como guía, no regla absoluta

---

## ⚠️ SOLUCIÓN DE PROBLEMAS

### Problemas Comunes y Soluciones

#### 1. **🔌 No puedo acceder al sistema**

**Síntomas:**
- Página no carga
- Error "No se puede acceder"

**Soluciones:**
1. ✅ Verificar que el servidor esté ejecutándose
2. ✅ Comprobar la dirección: `http://127.0.0.1:5000`
3. ✅ Probar con otro navegador
4. ✅ Contactar soporte técnico

#### 2. **📝 Errores al llenar el formulario**

**Síntomas:**
- Campos marcados en rojo
- Mensajes de error

**Soluciones:**
1. ✅ Verificar que todos los campos obligatorios estén llenos
2. ✅ Confirmar que los números estén en formato correcto
3. ✅ Revisar rangos válidos (ej: edad 18-80)
4. ✅ Usar puntos para decimales, no comas

#### 3. **⏳ Predicción muy lenta**

**Síntomas:**
- Tarda más de 10 segundos
- Sistema no responde

**Soluciones:**
1. ✅ Esperar un momento más (puede estar procesando)
2. ✅ Refrescar la página (F5)
3. ✅ Verificar conexión a internet
4. ✅ Intentar nuevamente

#### 4. **📊 Dashboard no actualiza**

**Síntomas:**
- Estadísticas desactualizadas
- Números no cambian

**Soluciones:**
1. ✅ Clic en "🔄 Actualizar"
2. ✅ Refrescar página completa
3. ✅ Verificar que se hayan hecho predicciones nuevas

#### 5. **🖨️ Problemas para imprimir**

**Síntomas:**
- Botón imprimir no funciona
- Formato inadecuado

**Soluciones:**
1. ✅ Usar Ctrl+P para impresión manual
2. ✅ Verificar configuración de impresora
3. ✅ Tomar captura de pantalla como alternativa

### Códigos de Error Comunes

| Código | Descripción | Solución |
|--------|-------------|----------|
| **E001** | Campos faltantes | Completar todos los campos requeridos |
| **E002** | Tipo de dato incorrecto | Verificar formato de números |
| **E003** | Valor fuera de rango | Revisar límites permitidos |
| **E404** | Modelo no encontrado | Contactar soporte técnico |
| **E500** | Error interno | Reintentar en unos minutos |

### ¿Cuándo Contactar Soporte?

**Contactar inmediatamente si:**
- ⚠️ El sistema muestra errores persistentes
- ⚠️ Las predicciones parecen incorrectas
- ⚠️ No se pueden guardar los resultados
- ⚠️ El sistema está completamente inaccesible

**Información a proporcionar:**
- 📝 Descripción detallada del problema
- 🖥️ Navegador y versión utilizada
- 📸 Capturas de pantalla del error
- 🕐 Hora y fecha del incidente
- 👤 Usuario que experimentó el problema

---

## 📞 SOPORTE Y CONTACTO

### Canales de Soporte

#### 🔧 **Soporte Técnico**
- **Email:** soporte@ahorrovalle.com
- **Teléfono:** +57 (2) 123-4567
- **Horario:** Lunes a Viernes, 8:00 AM - 6:00 PM

#### 📚 **Capacitación y Entrenamiento**
- **Email:** capacitacion@ahorrovalle.com
- **Solicitar:** Sesiones de entrenamiento
- **Incluye:** Manuales adicionales y videos

#### 💼 **Soporte de Negocio**
- **Email:** riesgos@ahorrovalle.com
- **Para:** Consultas sobre políticas crediticias
- **Incluye:** Interpretación de resultados complejos

### Recursos Adicionales

#### 📖 **Documentación Técnica**
- Manual técnico completo
- Guías de instalación y configuración
- Documentación de API

#### 🎥 **Videos Tutoriales**
- Cómo realizar predicciones
- Interpretación de resultados
- Casos de uso avanzados

#### 🤝 **Comunidad de Usuarios**
- Foro interno para usuarios
- Mejores prácticas compartidas
- Preguntas frecuentes

### Actualizaciones del Sistema

#### 📢 **Notificaciones**
- Se notificará por email sobre actualizaciones
- Nuevas funcionalidades se documentarán
- Cambios importantes se comunicarán con anticipación

#### 🔄 **Mantenimiento Programado**
- **Horario:** Domingos 2:00 AM - 4:00 AM
- **Notificación:** 48 horas de anticipación
- **Duración típica:** 1-2 horas

---

## 🎓 CONSEJOS PARA USUARIOS AVANZADOS

### Optimización del Flujo de Trabajo

#### 1. **Preparación de Datos**
- ✅ Tener toda la documentación antes de empezar
- ✅ Usar formato estándar para números
- ✅ Verificar información con el cliente

#### 2. **Interpretación Experta**
- ✅ Considerar contexto económico actual
- ✅ Evaluar factores no capturados por el modelo
- ✅ Usar predicción como herramienta, no decisión final

#### 3. **Documentación**
- ✅ Registrar decisiones y justificaciones
- ✅ Mantener historial de casos especiales
- ✅ Usar comentarios para casos complejos

### Mejores Prácticas

#### ✅ **Hacer**
- Verificar coherencia de datos ingresados
- Revisar advertencias del sistema
- Documentar decisiones no alineadas con predicción
- Usar modo demo para entrenamiento
- Mantener confidencialidad de datos

#### ❌ **No Hacer**
- Ignorar advertencias de validación
- Tomar decisiones basándose solo en la predicción
- Ingresar datos falsos o aproximados
- Compartir credenciales de acceso
- Procesar datos de clientes sin autorización

---

## 📝 REGISTRO DE ACTIVIDADES

### ¿Qué se Registra?

El sistema automáticamente registra:
- ✅ **Todas las predicciones realizadas**
- ✅ **Fecha y hora de cada consulta**
- ✅ **Datos de entrada (anónimos)**
- ✅ **Resultados obtenidos**
- ✅ **Usuario que realizó la consulta**

### Propósito del Registro

- 📊 **Auditoría:** Cumplimiento regulatorio
- 📈 **Análisis:** Mejora continua del modelo
- 🔍 **Seguimiento:** Monitoreo de decisiones
- 🎯 **Capacitación:** Casos de estudio

### Confidencialidad

- 🔒 **Datos protegidos** según normativas vigentes
- 🛡️ **Acceso restringido** a personal autorizado
- 📋 **Cumplimiento** con políticas de privacidad
- 🗂️ **Retención** según políticas internas

---

## 🚀 PRÓXIMAS FUNCIONALIDADES

### En Desarrollo

#### 📱 **Versión Móvil**
- Aplicación para tablets y smartphones
- Funcionalidad completa en dispositivos móviles
- Sincronización con versión web

#### 🤖 **Inteligencia Aumentada**
- Análisis de documentos automático
- Detección de inconsistencias
- Sugerencias proactivas

#### 📊 **Reportes Avanzados**
- Dashboards personalizables
- Exportación a Excel/PDF
- Análisis de tendencias mensuales

### Solicitar Nuevas Funcionalidades

¿Tiene ideas para mejorar el sistema?
- 📧 **Email:** desarrollo@ahorrovalle.com
- 📝 **Incluir:** Descripción detallada
- 🎯 **Beneficio:** Cómo mejoraría su trabajo
- 📊 **Prioridad:** Qué tan importante es

---

**📋 Resumen del Manual:**

✅ **Acceso Simple**: URL directa, navegador estándar
✅ **Proceso Claro**: 6 secciones organizadas, validación automática  
✅ **Resultados Comprensibles**: Predicción + Riesgo + Recomendación
✅ **Dashboard Útil**: Estadísticas en tiempo real
✅ **Modo Demo**: Ejemplos para aprendizaje
✅ **Soporte Completo**: Múltiples canales de ayuda
✅ **Mejores Prácticas**: Guías para uso profesional

*Este manual está diseñado para que cualquier usuario pueda aprovechar al máximo el Sistema de Predicción de Morosidad de Ahorro Valle.*

**Última actualización:** 28 de Octubre, 2025
**Versión del Manual:** 1.0