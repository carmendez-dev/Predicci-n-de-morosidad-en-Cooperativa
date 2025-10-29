// Script principal para la predicción de morosidad

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('prediccion-form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            realizarPrediccion();
        });
    }
    
    // Cargar perfil precargado si existe
    cargarPerfilPrecargado();
});

// Función eliminada - los campos son ahora completamente libres

function cargarPerfilPrecargado() {
    const perfilData = sessionStorage.getItem('perfilPrecargado');
    
    if (perfilData) {
        const perfil = JSON.parse(perfilData);
        
        // Rellenar todos los campos del formulario
        for (const [campo, valor] of Object.entries(perfil)) {
            const input = document.getElementById(campo);
            if (input) {
                input.value = valor;
                // Resaltar campos pre-cargados
                input.style.backgroundColor = '#fffacd';
                setTimeout(() => {
                    input.style.backgroundColor = '';
                }, 3000);
            }
        }
        
        // Limpiar sessionStorage
        sessionStorage.removeItem('perfilPrecargado');
        
        // Mostrar mensaje
        alert('✅ Datos del perfil de ejemplo cargados. Puedes modificarlos o hacer clic en "Predecir Morosidad".');
        
        // Scroll al formulario
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}


function validarFormulario() {
    // Campos que deben ser numéricos
    const camposNumericos = [
        'edad', 'antiguedad', 'ingresos', 'score_crediticio', 
        'pagos_previos', 'creditos_previos', 'monto_credito', 
        'valor_garantia', 'precio_soya', 'precio_vino', 'uso_productos'
    ];
    
    let esValido = true;
    
    camposNumericos.forEach(id => {
        const input = document.getElementById(id);
        if (input) {
            const valor = parseFloat(input.value);
            
            // Limpiar estilos previos
            input.style.borderColor = '';
            
            // Validaciones básicas solo al enviar
            if (!input.value || input.value === '' || isNaN(valor)) {
                input.style.borderColor = '#e74c3c';
                esValido = false;
            } else if (valor < 0) {
                input.style.borderColor = '#e74c3c';
                esValido = false;
                alert(`El campo ${input.previousElementSibling.textContent} no puede ser negativo.`);
            } else {
                input.style.borderColor = '#27ae60';
            }
        }
    });
    
    return esValido;
}

async function realizarPrediccion() {
    // Validar formulario antes de enviar
    if (!validarFormulario()) {
        alert('Por favor, complete todos los campos numéricos con valores válidos (números positivos).');
        return;
    }
    
    // Mostrar loading
    document.getElementById('loading').style.display = 'block';
    document.getElementById('resultado-container').style.display = 'none';
    
    // Recopilar datos del formulario
    const formData = {
        edad: parseInt(document.getElementById('edad').value),
        genero: document.getElementById('genero').value,
        zona: document.getElementById('zona').value,
        tipo_empleo: document.getElementById('tipo_empleo').value,
        antiguedad: parseInt(document.getElementById('antiguedad').value),
        ingresos: parseFloat(document.getElementById('ingresos').value),
        score_crediticio: parseFloat(document.getElementById('score_crediticio').value),
        pagos_previos: parseInt(document.getElementById('pagos_previos').value),
        creditos_previos: parseInt(document.getElementById('creditos_previos').value),
        monto_credito: parseFloat(document.getElementById('monto_credito').value),
        plazo_meses: parseInt(document.getElementById('plazo_meses').value),
        destino_credito: document.getElementById('destino_credito').value,
        tipo_garantia: document.getElementById('tipo_garantia').value,
        valor_garantia: parseFloat(document.getElementById('valor_garantia').value),
        precio_soya: parseFloat(document.getElementById('precio_soya').value),
        precio_vino: parseFloat(document.getElementById('precio_vino').value),
        uso_productos: parseInt(document.getElementById('uso_productos').value)
    };
    
    try {
        // Enviar petición al servidor
        const response = await fetch('/predecir', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        // Ocultar loading
        document.getElementById('loading').style.display = 'none';
        
        if (response.ok) {
            // Mostrar resultado
            mostrarResultado(resultado);
        } else {
            // Mostrar error
            alert('Error: ' + (resultado.error || 'Error desconocido'));
        }
        
    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert('Error de conexión: ' + error.message);
    }
}

function mostrarResultado(resultado) {
    // Configurar el título
    const titulo = resultado.prediccion_texto;
    document.getElementById('resultado-titulo').textContent = titulo;
    
    // Configurar el badge
    const badge = document.getElementById('resultado-badge');
    badge.textContent = titulo;
    badge.className = 'badge ' + (resultado.prediccion === 1 ? 'moroso' : 'no-moroso');
    
    // Configurar probabilidades
    const probNoMoroso = (resultado.probabilidad_no_moroso * 100).toFixed(2);
    const probMoroso = (resultado.probabilidad_moroso * 100).toFixed(2);
    
    document.getElementById('prob-no-moroso').textContent = probNoMoroso + '%';
    document.getElementById('prob-moroso').textContent = probMoroso + '%';
    
    // Animar barras de progreso
    setTimeout(() => {
        document.getElementById('prob-no-moroso-bar').style.width = probNoMoroso + '%';
        document.getElementById('prob-moroso-bar').style.width = probMoroso + '%';
    }, 100);
    
    // Configurar nivel de riesgo
    const nivelRiesgo = document.getElementById('nivel-riesgo');
    nivelRiesgo.textContent = resultado.riesgo;
    nivelRiesgo.className = resultado.riesgo.toLowerCase().replace(' ', '-');
    
    // Configurar recomendación
    document.getElementById('texto-recomendacion').textContent = resultado.recomendacion;
    
    // Configurar timestamp
    document.getElementById('timestamp').textContent = resultado.timestamp;
    
    // Mostrar el contenedor de resultados con animación
    const resultadoContainer = document.getElementById('resultado-container');
    resultadoContainer.style.display = 'block';
    
    // Scroll suave hacia el resultado
    resultadoContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function nuevaPrediccion() {
    // Ocultar resultado
    document.getElementById('resultado-container').style.display = 'none';
    
    // Limpiar formulario
    document.getElementById('prediccion-form').reset();
    
    // Scroll hacia arriba
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function imprimirResultado() {
    window.print();
}

// Campos completamente libres - sin validaciones restrictivas

// Formateo automático de montos
function formatearMoneda(input) {
    let valor = input.value.replace(/[^\d.]/g, '');
    if (valor) {
        input.value = parseFloat(valor).toFixed(2);
    }
}

// Auto-completar valores sugeridos basados en el tipo de empleo
document.addEventListener('DOMContentLoaded', function() {
    const tipoEmpleoSelect = document.getElementById('tipo_empleo');
    const ingresosInput = document.getElementById('ingresos');
    
    if (tipoEmpleoSelect && ingresosInput) {
        tipoEmpleoSelect.addEventListener('change', function() {
            const ingresosSugeridos = {
                'Dependiente': 4500,
                'Independiente': 4000,
                'Agricola': 3500,
                'Gobierno': 5000
            };
            
            if (!ingresosInput.value && this.value in ingresosSugeridos) {
                ingresosInput.value = ingresosSugeridos[this.value];
                ingresosInput.style.backgroundColor = '#fffacd';
                setTimeout(() => {
                    ingresosInput.style.backgroundColor = '';
                }, 2000);
            }
        });
    }
});

// Valores sugeridos para variables económicas
document.addEventListener('DOMContentLoaded', function() {
    const precioSoyaInput = document.getElementById('precio_soya');
    const precioVinoInput = document.getElementById('precio_vino');
    
    // Sugerir valores promedio si están vacíos al hacer focus
    if (precioSoyaInput) {
        precioSoyaInput.addEventListener('focus', function() {
            if (!this.value) {
                this.placeholder = 'Valor sugerido: 420.90';
            }
        });
    }
    
    if (precioVinoInput) {
        precioVinoInput.addEventListener('focus', function() {
            if (!this.value) {
                this.placeholder = 'Valor sugerido: 48.08';
            }
        });
    }
});

// Calcular automáticamente el valor de la garantía sugerido
document.addEventListener('DOMContentLoaded', function() {
    const montoCreditoInput = document.getElementById('monto_credito');
    const valorGarantiaInput = document.getElementById('valor_garantia');
    const tipoGarantiaSelect = document.getElementById('tipo_garantia');
    
    if (montoCreditoInput && valorGarantiaInput && tipoGarantiaSelect) {
        montoCreditoInput.addEventListener('blur', function() {
            if (this.value && tipoGarantiaSelect.value && !valorGarantiaInput.value) {
                let porcentaje = 1.0;
                
                switch(tipoGarantiaSelect.value) {
                    case 'Inmueble':
                        porcentaje = 1.2;
                        break;
                    case 'Vehiculo':
                        porcentaje = 1.1;
                        break;
                    case 'Ninguna':
                        porcentaje = 0.8;
                        break;
                }
                
                const valorSugerido = (parseFloat(this.value) * porcentaje).toFixed(2);
                valorGarantiaInput.value = valorSugerido;
                valorGarantiaInput.style.backgroundColor = '#fffacd';
                setTimeout(() => {
                    valorGarantiaInput.style.backgroundColor = '';
                }, 2000);
            }
        });
    }
});
