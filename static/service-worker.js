/**
 * Service Worker - FUTMAX PWA
 * Caching e offline support com synchronization
 */

const CACHE_NAME = 'futmax-v2';
const ASSETS_TO_CACHE = [
    '/',
    '/static/style.css',
    '/static/utilities.js',
    '/static/manifest.json',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css',
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap',
    'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.js'
];

// Instalar Service Worker
self.addEventListener('install', (event) => {
    console.log('[Service Worker] Instalando...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[Service Worker] Cacheando assets');
                return cache.addAll(ASSETS_TO_CACHE);
            })
            .catch(err => console.error('[Service Worker] Erro ao cachear:', err))
    );
    
    self.skipWaiting();
});

// Ativar Service Worker
self.addEventListener('activate', (event) => {
    console.log('[Service Worker] Ativando...');
    
    event.waitUntil(
        caches.keys()
            .then((cacheNames) => {
                return Promise.all(
                    cacheNames
                        .filter((cacheName) => cacheName !== CACHE_NAME)
                        .map((cacheName) => {
                            console.log('[Service Worker] Deletando cache antigo:', cacheName);
                            return caches.delete(cacheName);
                        })
                );
            })
    );
    
    self.clients.claim();
});

// Interceptar requisições
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Ignorar requisições non-GET
    if (request.method !== 'GET') {
        return;
    }
    
    // Ignorar requisições para o servidor de API (deixar atualizar)
    if (url.hostname === 'api.football-data.org') {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // Cachear resposta para uso offline
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    // Voltar para cache se offline
                    return caches.match(request);
                })
        );
        return;
    }
    
    // Stratégia Cache First para assets estáticos
    if (request.destination === 'style' || 
        request.destination === 'script' ||
        request.destination === 'font') {
        event.respondWith(
            caches.match(request)
                .then((response) => {
                    if (response) {
                        return response;
                    }
                    return fetch(request).then((response) => {
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME).then((cache) => {
                            cache.put(request, responseClone);
                        });
                        return response;
                    });
                })
                .catch(() => {
                    console.error('[Service Worker] Erro ao buscar recurso:', request.url);
                })
        );
        return;
    }
    
    // Estratégia Network First para páginas HTML
    event.respondWith(
        fetch(request)
            .then((response) => {
                if (response.status === 200) {
                    const responseClone = response.clone();
                    caches.open(CACHE_NAME).then((cache) => {
                        cache.put(request, responseClone);
                    });
                }
                return response;
            })
            .catch(() => {
                return caches.match(request)
                    .then((response) => {
                        if (response) {
                            return response;
                        }
                        // Página offline
                        return new Response(
                            '<html><body><h1>Sem conexão</h1><p>Verifique sua internet e tente novamente.</p></body></html>',
                            { headers: { 'Content-Type': 'text/html' } }
                        );
                    });
            })
    );
});

// Mensagens do cliente
self.addEventListener('message', (event) => {
    if (event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
    
    if (event.data.type === 'CLEAR_CACHE') {
        caches.delete(CACHE_NAME).then(() => {
            console.log('[Service Worker] Cache limpo');
        });
    }
});

console.log('[Service Worker] Carregado');
