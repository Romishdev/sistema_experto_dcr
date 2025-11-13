
function toggleSelect(enable) {
    const selectElement = document.getElementById('tipo_exp_paciente');
    selectElement.disabled = !enable;
    if (!enable) {
        selectElement.value = "";
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const siChecked = document.getElementById('exp_reciente_paciente_t').checked;
    toggleSelect(siChecked);
});

// Detecta cuándo los elementos con la clase 'fade-item' entran en el viewport

document.addEventListener('DOMContentLoaded', () => {
    const fadeItems = document.querySelectorAll('.fade-item');

    // 1. Define la función de observador (callback)
    const observerCallback = (entries, observer) => {
        entries.forEach(entry => {
            // Si el elemento es visible (es decir, intersecta el viewport)
            if (entry.isIntersecting) {
                // 2. Agrega la clase 'is-visible' para activar la transición CSS
                entry.target.classList.add('is-visible');

                // 3. Opcional: Deja de observar el elemento, ya que ya apareció
                observer.unobserve(entry.target);
            }
        });
    };

    // 4. Configuración del observador
    const observerOptions = {
        root: null, // Usa el viewport como root
        threshold: 0.1 // El elemento es visible cuando al menos el 10% está en pantalla
    };

    // 5. Crea y aplica el observador
    const observer = new IntersectionObserver(observerCallback, observerOptions);

    fadeItems.forEach(item => {
        observer.observe(item);
    });
});