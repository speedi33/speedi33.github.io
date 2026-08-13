const CACHE_NAME = 'foodreminder-v1';
const CDN_CACHE_NAME = 'foodreminder-cdn-v1';
const CDN_PREFIX = 'https://cdn.jsdelivr.net/';
const PRECACHE_URLS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './favicon.ico',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key !== CACHE_NAME && key !== CDN_CACHE_NAME)
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

function isSameOrigin(request) {
  return new URL(request.url, self.location.href).origin === self.location.origin;
}

function isNavigation(request) {
  return request.mode === 'navigate';
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  if (request.url.startsWith(CDN_PREFIX)) {
    event.respondWith(
      caches.open(CDN_CACHE_NAME).then(async (cache) => {
        const cached = await cache.match(request);
        if (cached) return cached;
        const network = await fetch(request);
        if (network && network.status === 200) {
          cache.put(request, network.clone());
        }
        return network;
      })
    );
    return;
  }

  if (!isSameOrigin(request)) return;

  event.respondWith(
    caches.open(CACHE_NAME).then(async (cache) => {
      if (isNavigation(request)) {
        try {
          const response = await fetch(request);
          cache.put('./index.html', response.clone());
          return response;
        } catch {
          return (await cache.match('./index.html')) || Response.error();
        }
      }

      const cached = await cache.match(request);
      const network = fetch(request)
        .then((response) => {
          if (response && response.status === 200 && response.type === 'basic') {
            cache.put(request, response.clone());
          }
          return response;
        })
        .catch(() => cached);
      return cached || network;
    })
  );
});

self.addEventListener('notificationclick', (event) => {
  event.notification.close();
  event.waitUntil(
    self.clients.matchAll({ type: 'window', includeUncontrolled: true }).then((clients) => {
      for (const client of clients) {
        if ('focus' in client) {
          client.focus();
          return;
        }
      }
      if (self.clients.openWindow) {
        return self.clients.openWindow('./');
      }
    })
  );
});

self.addEventListener('push', (event) => {
  let data = { title: 'FoodReminder', body: 'Lebensmittel-Erinnerung' };
  if (event.data) {
    try {
      data = Object.assign(data, event.data.json());
    } catch {
      data.body = event.data.text() || data.body;
    }
  }
  event.waitUntil(
    self.registration.showNotification(data.title, {
      body: data.body,
      icon: './icon-192.png',
      badge: './icon-192.png',
    })
  );
});
