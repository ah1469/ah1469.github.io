const CACHE_NAME = 'adam-portfolio-v3';
const APP_SHELL = [
  '/',
  '/index.html',
  '/projects/',
  '/experience/',
  '/skills/',
  '/styles.css',
  '/app.js',
  '/manifest.webmanifest',
  '/favicon.svg',
  '/assets/fonts/LiberationSans-Regular.ttf',
  '/assets/fonts/LiberationSans-Italic.ttf',
  '/assets/fonts/LiberationSans-Bold.ttf',
  '/assets/fonts/LiberationSans-BoldItalic.ttf',
  '/assets/fonts/LICENSE-Liberation-Sans.txt',
  '/output/pdf/Adam_Hemmouda_Resume_Public.pdf'
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(
      keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
    ))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET' || new URL(event.request.url).origin !== self.location.origin) return;

  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request).catch(async () => (
        await caches.match(event.request) || await caches.match('/index.html')
      ))
    );
    return;
  }

  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request).then((response) => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
      return response;
    }))
  );
});
