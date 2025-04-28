// static/service-worker.js

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('pwa-cache').then(function(cache) {
            return cache.addAll([
                '/',
                '/static/css/styles.css',
                '/static/js/main.js',
                '/static/icons/icon-192x192.png',
                '/static/icons/icon-512x512.png',
                // Añadir otros archivos estáticos necesarios
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || fetch(event.request);
        })
    );
});
