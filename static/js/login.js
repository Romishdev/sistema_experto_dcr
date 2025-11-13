// /static/js/login.js

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');
    
    if (!loginForm) return; // Asegura que el formulario existe

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // IMPORTANTE: Previene la recarga de página por defecto

        // Oculta cualquier mensaje de error previo
        errorMessage.textContent = '';
        errorMessage.classList.add('hidden-error');

        // 1. Captura los datos del formulario
        const formData = new FormData(loginForm);
        
        try {
            // 2. Envía la solicitud POST a Flask
            const response = await fetch('/iniciar-sesion', {
                method: 'POST',
                body: formData // Envía los datos como multipart/form-data
            });

            const data = await response.json(); // Parsea la respuesta JSON de Flask

            if (data.success) {
                // 3. Éxito: Redirige al usuario (si Flask devolvió success=True)
                window.location.href = data.redirect_url;
            } else {
                // 4. Fallo: Muestra el mensaje de error de Flask
                // Usamos el alert (como pediste) y mostramos el error en la tarjeta.
                alert(data.message); 
                
                errorMessage.textContent = data.message;
                errorMessage.classList.remove('hidden-error');
            }
        } catch (error) {
            console.error('Error de red o del servidor:', error);
            alert('Ocurrió un error al intentar iniciar sesión. Por favor, revisa tu conexión.');
        }
    });
});

// La función 'mostrarMensajeInvalido' ya no es necesaria con AJAX, 
// ya que el error se maneja en el listener del submit.