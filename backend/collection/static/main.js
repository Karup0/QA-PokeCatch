// static/js/main.js

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function() {
        navigator.serviceWorker.register('/static/service-worker.js').then(function(registration) {
            console.log('Service Worker registrado con éxito:', registration);
        }).catch(function(error) {
            console.log('Error al registrar el Service Worker:', error);
        });
    });
}
