// Script para la página de estadísticas

document.addEventListener('DOMContentLoaded', function() {
    cargarEstadisticas();
    
    // Auto-actualizar cada 30 segundos
    setInterval(cargarEstadisticas, 30000);
});

async function cargarEstadisticas() {
    try {
        const response = await fetch('/api/estadisticas');
        const datos = await response.json();
        
        if (response.ok) {
            actualizarInterfaz(datos);
        } else {
            console.error('Error al cargar estadísticas:', datos.error);
        }
    } catch (error) {
        console.error('Error de conexión:', error);
    }
}

function actualizarInterfaz(datos) {
    // Actualizar contadores
    document.getElementById('total-predicciones').textContent = datos.total || 0;
    document.getElementById('no-morosos').textContent = datos.no_morosos || 0;
    document.getElementById('morosos').textContent = datos.morosos || 0;
    
    // Actualizar probabilidad promedio
    const probPromedio = datos.prob_moroso_promedio || 0;
    document.getElementById('prob-promedio').textContent = (probPromedio * 100).toFixed(1) + '%';
    
    // Actualizar última predicción
    const ultimaPrediccion = datos.ultima_prediccion || 'N/A';
    document.getElementById('ultima-prediccion').textContent = ultimaPrediccion;
    
    // Actualizar gráfico (simple con divs por ahora)
    actualizarGrafico(datos);
}

function actualizarGrafico(datos) {
    const canvas = document.getElementById('prediccionesChart');
    if (!canvas) return;
    
    // Crear visualización simple con barras CSS
    const total = datos.total || 1; // Evitar división por cero
    const porcentajeNoMorosos = ((datos.no_morosos || 0) / total) * 100;
    const porcentajeMorosos = ((datos.morosos || 0) / total) * 100;
    
    const graficoHTML = `
        <div style="max-width: 600px; margin: 20px auto;">
            <div style="margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold;">No Morosos</span>
                    <span style="font-weight: bold;">${porcentajeNoMorosos.toFixed(1)}%</span>
                </div>
                <div style="background: #ecf0f1; height: 40px; border-radius: 20px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #27ae60, #2ecc71); height: 100%; width: ${porcentajeNoMorosos}%; transition: width 1s ease;"></div>
                </div>
            </div>
            
            <div style="margin-bottom: 30px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                    <span style="font-weight: bold;">Morosos</span>
                    <span style="font-weight: bold;">${porcentajeMorosos.toFixed(1)}%</span>
                </div>
                <div style="background: #ecf0f1; height: 40px; border-radius: 20px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #e74c3c, #c0392b); height: 100%; width: ${porcentajeMorosos}%; transition: width 1s ease;"></div>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <p style="font-size: 1.2em; margin: 0;">
                    <strong>Total de Evaluaciones:</strong> ${datos.total || 0}
                </p>
            </div>
        </div>
    `;
    
    canvas.outerHTML = '<div id="prediccionesChart">' + graficoHTML + '</div>';
}

function actualizarEstadisticas() {
    // Mostrar feedback visual
    const btn = event.target;
    const textoOriginal = btn.textContent;
    btn.textContent = 'Actualizando...';
    btn.disabled = true;
    
    cargarEstadisticas().then(() => {
        btn.textContent = textoOriginal;
        btn.disabled = false;
        
        // Mostrar mensaje temporal
        btn.textContent = 'Actualizado';
        setTimeout(() => {
            btn.textContent = textoOriginal;
        }, 2000);
    });
}
