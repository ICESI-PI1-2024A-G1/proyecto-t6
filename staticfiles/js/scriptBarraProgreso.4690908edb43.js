// Función para establecer el progreso del círculo
function setProgress(eventId, percent) {
    const circle = document.querySelector(`#circle_${eventId} .progress-ring-circle`);
    const radius = circle.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;

    const offset = circumference - (percent / 100) * circumference;
    circle.style.strokeDasharray = `${circumference} ${circumference}`;
    circle.style.strokeDashoffset = offset;

    const progressText = document.getElementById(`progressText_${eventId}`);
    progressText.textContent = `${percent}%`;
}

// Obtener los IDs de los círculos de carga
function cargarBarra(eventId, estado_alimentacion, estado_transporte, estado_extra) {
    alimentacion = estado_alimentacion == "True" ? 100 / 3 : 0;
    transporte = estado_transporte == "True" ? 100/3 : 0;
    extra = estado_extra == "True" ? 100 / 3 : 0;

    setProgress(eventId, parseInt(alimentacion + transporte + extra)); // Cambia el porcentaje según sea necesario
}
