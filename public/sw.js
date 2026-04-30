const CACHE_NAME = 'hospital-survey-v1';
const ASSETS = [
    '/index.php',
    '/style.css',
    '/script.js',
    '/manifest.json'
];

self.addEventListener('install', e => {
    e.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
    );
    self.skipWaiting();
});

self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
    self.clients.claim();
});

self.addEventListener('fetch', e => {
    // Only cache GET requests, let POST (form submit) go through normally
    if (e.request.method !== 'GET') return;

    e.respondWith(
        caches.match(e.request).then(cached => cached || fetch(e.request))
    );
});
