/**
 * FUTMAX - Utilities JavaScript
 * Funções auxiliares para animações, notificações e efeitos visuais
 */

// ===== NOTIFICAÇÕES (Toast) =====

/**
 * Mostrar notificação toast
 * @param {string} mensagem - Texto da notificação
 * @param {string} tipo - 'success', 'error', 'warning', 'info'
 * @param {number} duracao - Duração em ms (0 = manual)
 */
function showToast(mensagem, tipo = 'info', duracao = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast show bg-${getTipoBgClass(tipo)}`;
    
    const icons = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };

    toast.innerHTML = `
        <div class="toast-body text-white">
            <strong>${icons[tipo] || 'ℹ️'}</strong> ${mensagem}
            <button type="button" class="btn-close btn-close-white ms-2" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;
    
    document.body.appendChild(toast);
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        min-width: 300px;
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
    `;
    
    if (duracao > 0) {
        setTimeout(() => {
            toast.style.animation = 'slideOutRight 0.3s ease-in';
            setTimeout(() => toast.remove(), 300);
        }, duracao);
    }
}

function getTipoBgClass(tipo) {
    const map = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return map[tipo] || 'info';
}

// ===== ANIMAÇÕES DE CARREGAMENTO =====

/**
 * Mostrar skeleton loader (substituir conteúdo por placeholder)
 * @param {string} seletor - ID ou classe do elemento
 * @param {number} linhas - Quantas linhas de skeleton mostrar
 */
function showSkeleton(seletor, linhas = 3) {
    const el = document.querySelector(seletor);
    if (!el) return;
    
    let html = '<div class="placeholder-glow">';
    for (let i = 0; i < linhas; i++) {
        html += '<div class="placeholder col-12 mb-2"></div>';
    }
    html += '</div>';
    
    el.innerHTML = html;
}

/**
 * Esconder skeleton e exibir conteúdo
 * @param {string} seletor - ID ou classe do elemento
 * @param {string} conteudo - HTML do conteúdo a exibir
 */
function hideSkeleton(seletor, conteudo) {
    const el = document.querySelector(seletor);
    if (!el) return;
    
    el.innerHTML = conteudo;
    el.style.animation = 'fadeInUp 0.3s ease-out';
}

// ===== SCROLL INFINITO =====

/**
 * Implementar scroll infinito (lazy loading)
 * @param {string} seletor - Classe ou ID dos itens a carregar
 * @param {function} callback - Função chamada quando reach bottom
 * @param {number} threshold - Pixels antes do fim para disparar
 */
function enableInfiniteScroll(seletor, callback, threshold = 500) {
    const options = {
        root: null,
        rootMargin: `${threshold}px`,
        threshold: 0
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback();
            }
        });
    }, options);
    
    const sentinela = document.querySelector(seletor);
    if (sentinela) observer.observe(sentinela);
    
    return observer;
}

// ===== MODAL CUSTOMIZADO =====

/**
 * Abrir modal customizado
 * @param {string} titulo - Título do modal
 * @param {string} conteudo - HTML do conteudo
 * @param {array} botoes - [{texto, classe, onclick}, ...]
 */
function openModal(titulo, conteudo, botoes = []) {
    const modalId = `modal-${Date.now()}`;
    
    let botoesHtml = '';
    botoes.forEach(btn => {
        botoesHtml += `<button class="btn ${btn.classe || 'btn-primary'}" onclick="${btn.onclick || ''}">${btn.texto}</button>`;
    });
    
    const modal = document.createElement('div');
    modal.id = modalId;
    modal.className = 'modal fade';
    modal.innerHTML = `
        <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">${titulo}</h5>
                    <button type="button" class="btn-close" onclick="document.getElementById('${modalId}').remove()"></button>
                </div>
                <div class="modal-body">
                    ${conteudo}
                </div>
                <div class="modal-footer">
                    ${botoesHtml}
                </div>
            </div>
        </div>
    `;
    
    document.body.appendChild(modal);
    new bootstrap.Modal(modal).show();
    
    return modal;
}

// ===== EFEITOS VISUAL =====

/**
 * Adicionar efeito ripple ao elemento
 * @param {HTMLElement} element - Elemento alvo
 */
function addRippleEffect(element) {
    element.addEventListener('click', (e) => {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.5);
            left: ${x}px;
            top: ${y}px;
            animation: ripple-animation 0.6s ease-out;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    });
}

// ===== LAZY LOADING DE IMAGENS =====

/**
 * Ativar lazy load para imagens
 */
function enableLazyLoadImages() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// ===== ANIMAÇÕES DE NÚMEROS =====

/**
 * Animar números (contador)
 * @param {string} seletor - Elemento contendo o número
 * @param {number} fim - Número final
 * @param {number} duracao - Duração em ms
 */
function animateNumber(seletor, fim, duracao = 1000) {
    const elemento = document.querySelector(seletor);
    if (!elemento) return;
    
    const inicio = parseInt(elemento.textContent) || 0;
    const incremento = (fim - inicio) / (duracao / 16);
    let atual = inicio;
    
    const interval = setInterval(() => {
        atual += incremento;
        if (atual >= fim) {
            elemento.textContent = fim;
            clearInterval(interval);
        } else {
            elemento.textContent = Math.floor(atual);
        }
    }, 16);
}

// ===== DARK MODE =====

/**
 * Alternar dark mode
 */
function toggleDarkMode() {
    const body = document.body;
    const isDark = body.getAttribute('data-theme') === 'dark';
    
    if (isDark) {
        body.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
    } else {
        body.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
    }
}

/**
 * Carregar tema salvo
 */
function initializeDarkMode() {
    const theme = localStorage.getItem('theme') || 'light';
    if (theme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
    }
}

// ===== DEBOUNCE =====

/**
 * Debounce function - evitar múltiplas chamadas
 * @param {function} func - Função a executar
 * @param {number} delay - Delay em ms
 */
function debounce(func, delay = 300) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// ===== THROTTLE =====

/**
 * Throttle function - limitar frequência de execução
 * @param {function} func - Função a executar
 * @param {number} limit - Limite em ms
 */
function throttle(func, limit = 300) {
    let lastFunc;
    let lastRan;
    return function(...args) {
        if (!lastRan) {
            func.apply(this, args);
            lastRan = Date.now();
        } else {
            clearTimeout(lastFunc);
            lastFunc = setTimeout(() => {
                if ((Date.now() - lastRan) >= limit) {
                    func.apply(this, args);
                    lastRan = Date.now();
                }
            }, limit - (Date.now() - lastRan));
        }
    };
}

// ===== OBSERVAR ELEMENTO EM VIEWPORT =====

/**
 * Executar função quando elemento entraar em viewport
 * @param {string} seletor - Elemento
 * @param {function} callback - Função a executar
 */
function onVisible(seletor, callback) {
    const element = document.querySelector(seletor);
    if (!element) return;
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                callback(entry.target);
                observer.unobserve(entry.target);
            }
        });
    });
    
    observer.observe(element);
}

// ===== ANIMAÇÕES DE PÁGINA =====

/**
 * Animar transição entre páginas
 * @param {string} url - URL para navegar
 * @param {number} duracao - Duração da animação
 */
function navigateWithAnimation(url, duracao = 300) {
    document.body.style.animation = `fadeOut ${duracao}ms ease-out`;
    setTimeout(() => {
        window.location.href = url;
    }, duracao);
}

/**
 * Animar entrada da página
 */
function animatePageLoad() {
    document.body.style.animation = 'fadeInUp 0.6s ease-out';
}

// ===== INICIALIZAÇÃO =====

// Executar ao carregar página
document.addEventListener('DOMContentLoaded', () => {
    initializeDarkMode();
    animatePageLoad();
    registerServiceWorker();
});

/**
 * Registrar Service Worker para PWA
 */
function registerServiceWorker() {
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/service-worker.js')
            .then(reg => {
                console.log('✅ Service Worker registrado');
                
                // Verificar atualizações
                setInterval(() => {
                    reg.update();
                }, 60000); // A cada minuto
                
                // Notificar quando houver update
                reg.addEventListener('updatefound', () => {
                    const newWorker = reg.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            showToast('Nova versão disponível! Recarregue a página.', 'info', 0);
                        }
                    });
                });
            })
            .catch(err => console.error('❌ Erro ao registrar Service Worker:', err));
    }
}

// Exportar para uso global
window.Utils = {
    showToast,
    openModal,
    showSkeleton,
    hideSkeleton,
    enableInfiniteScroll,
    addRippleEffect,
    enableLazyLoadImages,
    animateNumber,
    toggleDarkMode,
    debounce,
    throttle,
    onVisible,
    navigateWithAnimation
};
