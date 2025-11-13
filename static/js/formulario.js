// El archivo JavaScript está listo para añadir funcionalidades,
// como la validación de campos o el manejo asíncrono del envío.

document.getElementById('contact-form').addEventListener('submit', function(event) {
    // Previene el envío por defecto del formulario (recarga de la página)
    event.preventDefault();

    // Aquí se ejecutaría la lógica de validación y envío de datos
    // a un servidor (ej. usando fetch o XMLHttpRequest).

    console.log('Formulario enviado (simulación).');
    // Ejemplo de cómo obtener un valor:
    // const name = document.getElementById('name').value;
    // console.log('Nombre:', name);

    // Puedes agregar una alerta o un mensaje de éxito/error aquí.
});