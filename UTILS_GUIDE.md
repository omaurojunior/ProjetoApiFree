% 🎓 GUIA DE IMPLEMENTAÇÃO - FUTMAX v3.0

## 📚 Como Usar as Novas Funcionalidades

### 1. Adicionar Notificação em Qualquer Página

```html
<!-- No seu template -->
<button onclick="Utils.showToast('Ação realizada!', 'success')">
    Clique aqui
</button>
```

### 2. Implementar Skeleton Loader em Fetch

```javascript
// Antes de carregar dados
Utils.showSkeleton('#meu-container', 5);

// Fazer requisição
fetch('/api/dados')
    .then(r => r.json())
    .then(data => {
        const html = `<div>...</div>`;
        Utils.hideSkeleton('#meu-container', html);
    })
    .catch(() => {
        Utils.showToast('Erro ao carregar', 'error');
    });
```

### 3. Abrir Modal Customizado

```javascript
Utils.openModal(
    'Confirmação',
    '<p>Deseja continuar?</p>',
    [
        {
            texto: 'Sim',
            classe: 'btn-success',
            onclick: 'myFunction()'
        },
        {
            texto: 'Não',
            classe: 'btn-danger',
            onclick: 'this.closest(".modal").querySelector(".btn-close").click()'
        }
    ]
);
```

### 4. Busca com Debounce (Pesquisa em Tempo Real)

```html
<input type="text" id="busca" placeholder="Buscar times...">

<script>
const buscar = Utils.debounce((valor) => {
    fetch(`/pesquisa?termo=${valor}`)
        .then(r => r.text())
        .then(html => {
            document.getElementById('resultados').innerHTML = html;
        });
}, 500); // Aguarda 500ms após parar de digitar

document.getElementById('busca').addEventListener('input', (e) => {
    buscar(e.target.value);
});
</script>
```

### 5. Animar Números (Contadores)

```html
<div>
    <h2>Gols: <span id="contador">0</span></h2>
</div>

<script>
// Animar para 50 em 2 segundos
Utils.animateNumber('#contador', 50, 2000);
</script>
```

### 6. Lazy Loading de Imagens

```html
<!-- Em vez de <img src="..."> use data-src -->
<img data-src="/imagem.jpg" class="img-fluid" loading="lazy">

<script>
Utils.enableLazyLoadImages();
</script>
```

### 7. Scroll Infinito (Paginação)

```html
<!-- Seu conteúdo aqui -->
<div id="items"></div>

<!-- Elemento sentinela (trigger para carregar mais) -->
<div id="sentinel"></div>

<script>
let pagina = 1;

Utils.enableInfiniteScroll('#sentinel', () => {
    pagina++;
    fetch(`/api/items?page=${pagina}`)
        .then(r => r.json())
        .then(dados => {
            dados.forEach(item => {
                const el = document.createElement('div');
                el.textContent = item.nome;
                document.getElementById('items').appendChild(el);
            });
        });
});
</script>
```

### 8. Efeito Ripple em Botões

```html
<button id="meu-btn" class="btn btn-primary">Clique</button>

<script>
Utils.addRippleEffect(document.getElementById('meu-btn'));
</script>
```

### 9. Observar Entrada em Viewport

```html
<div id="card-especial">Card que ativa algo ao ficar visível</div>

<script>
Utils.onVisible('#card-especial', (elemento) => {
    elemento.style.animation = 'slideInUp 0.6s ease-out';
    console.log('Card ficou visível!');
});
</script>
```

### 10. Navegar com Animação de Transição

```html
<a onclick="Utils.navigateWithAnimation('/novapage', 300)">
    Ir para nova página
</a>
```

---

## 🎨 Usar Animações CSS

### Nas Templates

```html
<!-- Entrada suave -->
<div class="animate-card">Conteúdo</div>

<!-- Efeito glassmorphism -->
<div class="glass-effect">Conteúdo com vidro</div>

<!-- Scale ao hover -->
<div class="scale-hover">Cresce ao passar mouse</div>

<!-- Badge pulsante -->
<span class="badge bg-danger badge-pulse">Importante</span>
```

### No CSS Customizado

```css
/* Usar funções de animação registradas */
.meu-elemento {
    animation: slideInUp 0.6s ease-out;
}

.meu-componente:hover {
    animation: bounce 0.6s ease-in-out;
}

/* Efeito glow */
.importante {
    animation: glow 2s ease-in-out infinite;
}
```

---

## 🔌 Usar APIs REST Novas

### Favoritos

```javascript
// Adicionar favorito
fetch('/api/favoritos', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ team_id: 123 })
})
.then(r => r.json())
.then(data => console.log(data));

// Remover favorito
fetch('/api/favoritos', {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ team_id: 123 })
})
.then(r => r.json())
.then(data => console.log(data));

// Listar favoritos (GET)
fetch('/api/favoritos')
    .then(r => r.json())
    .then(data => console.log('Favoritos:', data.favoritos));
```

### Comparar Times

```javascript
const team1 = prompt('ID do Time 1:');
const team2 = prompt('ID do Time 2:');

fetch('/api/comparar', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ team1_id: team1, team2_id: team2 })
})
.then(r => r.json())
.then(comparacao => {
    console.log('Time 1:', comparacao.time1);
    console.log('Time 2:', comparacao.time2);
    
    // Exibir resultado
    Utils.showToast(
        `${comparacao.time1.nome} vs ${comparacao.time2.nome}`,
        'info'
    );
});
```

### Rankings

```javascript
// Ranking por pontos
fetch('/api/ranking?tipo=pontos')
    .then(r => r.json())
    .then(ranking => {
        ranking.forEach((time, i) => {
            console.log(`${i+1}º ${time.time} - ${time.pontos} pts`);
        });
    });

// Ranking por gols
fetch('/api/ranking?tipo=gols')
    .then(r => r.json())
    .then(ranking => console.log('Ranking de gols:', ranking));

// Ranking por defesa
fetch('/api/ranking?tipo=defesa')
    .then(r => r.json())
    .then(ranking => console.log('Ranking de defesa:', ranking));
```

---

## 🌙 Gerenciar Dark Mode

```javascript
// Alternar entre light/dark
Utils.toggleDarkMode();

// O localStorage salva automaticamente
localStorage.getItem('theme'); // 'light' ou 'dark'

// Inicializar ao carregar (já feito automaticamente)
Utils.initializeDarkMode();
```

---

## 📱 Testar PWA

### No Chrome DevTools
1. F12 > Application > Service Workers
2. Verificar se está "activated and running"
3. Clicar em "Update" para forçar atualização

### Em Dispositivo Real
1. Abrir em navegador móvel
2. Menu (⋮) > "Instalar app"
3. Confirmar instalação
4. App aparecerá na tela inicial

### Offline
1. DevTools > Network > Offline
2. Navegação continua funcionando
3. Dados em cache são exibidos

---

## 🐛 Debug & Troubleshooting

### Console Logs

```javascript
// Service Worker
console.log('✅ Service Worker registrado');

// API calls
console.log('API Call: /endpoint');

// Erros
console.error('❌ Erro ao carregar:', error);
```

### Network Tab (DevTools)
- Verificar requisições bloqueadas
- Cacheing funcionando (status 304)
- Size: "from disk cache" = cache ativo

### Storage Tab (DevTools)
- localStorage: verificar favoritos, tema
- indexedDB: dados em cache
- Service Workers: status "activated"

---

## 🎯 Exemplo Completo: Página de Busca

```html
{% extends 'base.html' %}
{% block content %}

<div class="container py-5">
    <h1>🔍 Busca Avançada</h1>
    
    <!-- Campo de busca com debounce -->
    <div class="mb-4">
        <input 
            type="text" 
            id="busca-input" 
            class="form-control form-control-lg"
            placeholder="Buscar times..."
        >
    </div>
    
    <!-- Skeleton enquanto carrega -->
    <div id="skeleton"></div>
    
    <!-- Resultados -->
    <div id="resultados"></div>
</div>

<script>
// Inicializar busca com debounce
const buscar = Utils.debounce((termo) => {
    if (!termo) {
        document.getElementById('resultados').innerHTML = '';
        return;
    }
    
    Utils.showSkeleton('#skeleton', 4);
    
    fetch(`/pesquisa`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `nome_time=${encodeURIComponent(termo)}`
    })
    .then(r => r.text())
    .then(html => {
        Utils.hideSkeleton('#skeleton', '');
        document.getElementById('resultados').innerHTML = html;
    })
    .catch(e => {
        Utils.showToast('Erro na busca', 'error');
        console.error(e);
    });
}, 400);

// Listener
document.getElementById('busca-input').addEventListener('input', (e) => {
    buscar(e.target.value);
});
</script>

{% endblock %}
```

---

## 📞 Suporte

Dúvidas? Verificar:
1. `utilities.js` - código das funções
2. `FEATURES_V3.md` - descrição completa
3. `app.py` - rotas Flask
4. Console do navegador - logs de erro

---

**Última atualização**: 3 de março de 2026
**Versão**: 3.0
