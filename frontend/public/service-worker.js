// service-worker.js — offline caching for static assets (#34).
//
// Strategy: cache-first for the app shell/static assets (fast repeat
// loads, works offline), network-first for API calls (/api/*), since
// engagement data must always be fresh when a connection exists, but a
// stale cached response is still better than nothing while offline.

const CACHE_NAME = "engageiq-static-v1";

// Precached on install. Vite fingerprints built JS/CSS bundle filenames,
// so we can't list them here ahead of time -- they're added to the cache
// opportunistically by the fetch handler below on first request instead.
const PRECACHE_URLS = [
  "/",
  "/manifest.json",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches
      .open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(
          keys
            .filter((key) => key !== CACHE_NAME)
            .map((key) => caches.delete(key))
        )
      )
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (event) => {
  const { request } = event;
  if (request.method !== "GET") return;

  const url = new URL(request.url);

  // API calls: network-first, don't cache -- engagement data is always
  // fresh when online, and caching student data offline would be a
  // privacy footgun for no real benefit.
  if (url.pathname.startsWith("/api/")) {
    event.respondWith(
      fetch(request).catch(
        () =>
          new Response(
            JSON.stringify({ error: "You're offline." }),
            { headers: { "Content-Type": "application/json" }, status: 503 }
          )
      )
    );
    return;
  }

  // Static assets (app shell, JS/CSS bundles, icons): cache-first, with
  // the network response cached opportunistically for next time.
  event.respondWith(
    caches.match(request).then((cached) => {
      if (cached) return cached;

      return fetch(request)
        .then((response) => {
          if (!response || response.status !== 200 || response.type === "opaque") {
            return response;
          }
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseClone));
          return response;
        })
        .catch(() => caches.match("/"));
    })
  );
});
