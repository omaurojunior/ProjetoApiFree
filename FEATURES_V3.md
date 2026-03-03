# ⚽ FUTMAX v3.0 - Novas Funcionalidades & Animações

## 🆕 Novas Rotas & Funcionalidades

### 1. **API REST Endpoints** 🔌
```bash
POST /api/favoritos          # Adicionar favorito
DELETE /api/favoritos        # Remover favorito
GET /api/favoritos           # Obter lista de favoritos

POST /api/comparar           # Comparar dois times
  Body: { team1_id, team2_id }
  Response: { time1: {...}, time2: {...} }

GET /api/ranking             # Ranking customizado
  Params: ?tipo=pontos|gols|defesa
  Response: [{ posicao, time, escudo, pontos, ... }]
```

### 2. **Comparador de Times** ⚔️
Nova página para comparar dois times lado a lado:
- Busca rápida por ID ou nome
- Skeleton loader durante carregamento
- Comparação de: fundação, estádio, número de jogadores
- Resultado visual intuitivo

**Acesso**: [Navbar] ⚔️ Comparador ou `/comparador`

### 3. **Ranking Avançado** 📊
Três tipos de ranking customizados:

#### **Ranking por Pontos** (Padrão)
- Ordenado por pontos
- Cores por zona (Libertadores 🟢, Pré-lib 🔵, Rebaixamento 🔴)
- Gráfico de barras interativo

#### **Ranking por Gols** 🎯
- Ordenado por gols a favor
- Mostra média de gols por jogo
- Gráfico de barras colorido

#### **Ranking por Defesa** 🛡️
- Ordenado por gols contra
- Mostra média de gols sofridos
- Identifica melhores defesas

**Acesso**: [Navbar] Rankings > [Pontos|Gols|Defesa]

---

## ✨ Animações Avançadas

### **1. Slide In Up** (Entrada de Elementos)
```css
animation: slideInUp 0.6s ease-out;
```
- Elementos entram de baixo para cima
- Usado em: cards, modals, conteúdo principal

### **2. Skeleton Loader** (Carregamento)
```css
@keyframes shimmer { ... }
animation: shimmer 2s infinite;
```
- Efeito de "brilho" enquanto carrega
- Substitui conteúdo durante fetch de dados
- Melhor UX do que spinner genérico

### **3. Pulse Animation** (Badges)
```css
@keyframes pulse { ... }
animation: badge-pulse 2s infinite;
```
- Badges pulsam suavemente
- Usado para alertas e notificações

### **4. Ripple Effect** (Clique em Botões)
```js
.btn::before {
    animation: ripple-animation 0.6s ease-out;
}
```
- Efeito estilo Material Design
- Feedback visual ao clicar

### **5. Glow Effect** (Cards Importantes)
```css
@keyframes glow { ... }
box-shadow: 0 0 20px rgba(0, 151, 57, 0.6);
```
- Efeito de brilho em cards destacados
- Usado em times favoritos da página comparador

### **6. Flip Card** (Hover)
```css
@keyframes flip { ... }
animation: flip 0.6s ease-in-out;
```
- Card se vira ao passar mouse
- Efeito 3D em elementos

### **7. Bounce** (Feedback)
```css
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
```
- Elemento salta levemente
- Usado para chamar atenção

---

## 🎯 Utilities JavaScript (`utilities.js`)

Funções prontas para usar em qualquer página:

### **Notificações**
```javascript
Utils.showToast('Mensagem', 'success', 3000);
// Tipos: 'success', 'error', 'warning', 'info'
```

### **Skeleton Loader**
```javascript
Utils.showSkeleton('#container', 3); // 3 linhas
// ... fazer fetch ...
Utils.hideSkeleton('#container', conteudo);
```

### **Modal Customizado**
```javascript
Utils.openModal('Título', '<p>Conteúdo</p>', [
    { texto: 'OK', classe: 'btn-primary', onclick: 'alert("ok")' }
]);
```

### **Lazy Loading de Imagens**
```javascript
// Na imagem HTML:
<img data-src="url.jpg" loading="lazy">

// Ativar:
Utils.enableLazyLoadImages();
```

### **Animação de Números**
```javascript
// Animar número de 0 a 100 em 1 segundo
Utils.animateNumber('#pontos', 100, 1000);
```

### **Dark Mode**
```javascript
Utils.toggleDarkMode(); // Alternar
```

### **Debounce & Throttle**
```javascript
// Evitar múltiplas chamadas
const buscar = Utils.debounce((termo) => {
    fetch(`/api/buscar?q=${termo}`);
}, 300);

// Limitar frequência
const scroll = Utils.throttle(() => {
    console.log('scroll');
}, 100);
```

### **Scroll Infinito**
```javascript
Utils.enableInfiniteScroll('.sentinela', () => {
    // Carregador mais items
});
```

---

## 📱 PWA (Progressive Web App)

### **Instalação em Dispositivos**
- ✅ Manifest.json configurado
- ✅ Service Worker para cache
- ✅ Ícones customizados
- ✅ Modo standalone (sem barra de navegador)

### **Como Instalar**
1. Acessar futmax.com em dispositivo móvel
2. Clicar no menu (⋮) > "Instalar app"
3. Confirmara instalação
4. App aparecerá na tela inicial

### **Shortcuts (Atalhos)**
Após instalar, adicionar atalhos rápidos para:
- ⚽ Resultados
- 📊 Classificação
- 🔍 Pesquisar

### **Offline Support**
- ✅ Funciona sem internet (dados em cache)
- ✅ Sinaliza quando voltar online
- ✅ Sincroniza automaticamente

---

## 🎨 Novos Estilos CSS

### **Glass Effect** (Efeito Vidro)
```css
.glass-effect {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}
```

### **Scale Hover**
```css
.scale-hover:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}
```

### **Gradient Backgrounds**
```css
background: linear-gradient(90deg, #009739, #fedd00, #009739);
background-size: 200% 100%;
animation: gradient-shift 3s ease-in-out infinite;
```

### **Smooth Transitions**
```css
* { transition: all 0.3s ease; }
```

---

## 📊 Nova Página: Comparador

### **Layout**
```
┌─────────────────────────────────────────┐
│          ⚔️ COMPARADOR DE TIMES         │
├──────────┬──────────────┬──────────────┤
│  Time 1  │   Comparar   │   Time 2     │
│  [Input] │      ⚔️      │  [Input]     │
│ [Info]   │   [Botão]    │  [Info]      │
└──────────┴──────────────┴──────────────┘
```

### **Funcionalidades**
- Busca de times por ID ou nome
- Skeleton loader durante carregamento
- Exibe: fundação, estádio, # jogadores, logo
- Comparação instantânea

---

## 📈 Nova Página: Ranking

### **Layout**
```
┌─────────────────────────────────────┐
│     🎯 RANKING [Tipo]              │
│  [Abas: Pontos|Gols|Defesa]        │
├─────────────────────────────────────┤
│     📊 Gráfico de Barras             │
├─────────────────────────────────────┤
│     📋 Tabela com Ranking            │
│   Pos | Time | Pontos | ... |       │
└─────────────────────────────────────┘
```

### **Dados Mostrados**

**Ranking Pontos:**
- Posição, Time, Pontos, Jogos, V, E, D

**Ranking Gols:**
- Posição, Time, Gols, Média/Jogo

**Ranking Defesa:**
- Posição, Time, Gols Contra, Média/Jogo

---

## 🔔 Sistema de Notificações

### **Toast em Tempo Real**
```javascript
// Sucesso
Utils.showToast('Favorito adicionado!', 'success');

// Erro
Utils.showToast('Erro ao carregar', 'error');

// Aviso
Utils.showToast('Limite de requisições', 'warning');

// Informação
Utils.showToast('Nova versão disponível', 'info');
```

### **Notificação de Update**
- Detecta nova versão do Service Worker
- Notifica usuário para recarregar
- Non-intrusive (pode ignorar)

---

## 🚀 Performance Melhorias

### **Caching Estratégias**
| Tipo | Estratégia | TTL |
|------|-----------|-----|
| CSS/JS | Cache First | Permanente |
| Imagens | Cache First | Permanente |
| API | Network First | 30 min cache |
| HTML | Network First | 5 min cache |

### **Lazy Loading**
- Imagens carregam sob demanda
- Economiza banda e acelera carregamento
- Placeholder animado

### **Code Splitting**
- utilities.js carregado uma vez
- CSS minificado
- Service Worker otimizado

---

## 📋 Checklist de Implementação

- ✅ API REST endpoints (favoritos, comparar, ranking)
- ✅ Página Comparador de Times
- ✅ Página Rankings (3 tipos)
- ✅ 15+ Animações CSS avançadas
- ✅ Utilities.js (20+ funções)
- ✅ PWA (Manifest + Service Worker)
- ✅ Novas rotas em Flask
- ✅ Dropdown menu na navbar
- ✅ Notificações toast
- ✅ Skeleton loaders

---

## 🎯 Próximas Melhorias (v4.0)

- [ ] Sincronização em tempo real (WebSocket)
- [ ] Notificações push para gols
- [ ] Gráficos avançados (Recharts)
- [ ] Dark mode melhorado
- [ ] Busca full-text com Elasticsearch
- [ ] Backend GraphQL
- [ ] Autenticação com OAuth
- [ ] Sistema de comentários
- [ ] Estatísticas por jogador
- [ ] Previsões com IA

---

**Versão**: 3.0
**Data**: 3 de março de 2026
**Status**: ✅ Pronto para uso
