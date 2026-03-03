# 🔧 GUIA DE IMPLEMENTAÇÃO - Sistema de Favoritos Persistente

## 📌 Visão Geral

O arquivo `database.py` fornece um sistema completo de persistência de favoritos e histórico de pesquisas usando SQLite.

## 🚀 Como Usar no app.py

### 1. Importar módulo
```python
from database import (
    adicionar_favorito, 
    remover_favorito, 
    obter_favoritos,
    adicionar_pesquisa,
    obter_historico_pesquisas
)
```

### 2. Integrar rota de favoritos
```python
@app.route('/api/favorito', methods=['POST'])
@limiter.limit("30 per minute")
def api_favorito():
    """API para adicionar/remover favoritos persisten temente."""
    data = request.json
    user_id = request.remote_addr  # Usar IP ou sessão de usuário
    team_id = data.get('team_id')
    action = data.get('action')  # 'add' ou 'remove'
    
    if action == 'add':
        sucesso = adicionar_favorito(user_id, team_id)
    elif action == 'remove':
        sucesso = remover_favorito(user_id, team_id)
    else:
        return jsonify({'erro': 'Ação inválida'}), 400
    
    return jsonify({'sucesso': sucesso})
```

### 3. Carregar favoritos ao iniciar
```python
@app.route('/')
def index():
    user_id = request.remote_addr
    favoritos = obter_favoritos(user_id)  # Lista de IDs
    
    # ... resto do código
    return render_template('index.html', 
                          matches=matches,
                          favoritos=favoritos)  # Passar para template
```

### 4. Integrar no template
```html
<script>
// Carregar favoritos do servidor
fetch('/api/favoritos')
    .then(r => r.json())
    .then(data => {
        localStorage.setItem('favTeams', JSON.stringify(data.favoritos));
    });

// Sincronizar ao adicionar/remover
window.toggleFavorito = function(teamId, element) {
    const action = element.classList.contains('active') ? 'remove' : 'add';
    
    fetch('/api/favorito', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({team_id: teamId, action: action})
    })
    .then(r => r.json())
    .then(data => {
        if (data.sucesso) {
            // Atualizar localStorage também
            let favs = JSON.parse(localStorage.getItem('favTeams') || '[]');
            if (action === 'add') {
                favs.push(teamId.toString());
            } else {
                favs = favs.filter(id => id !== teamId.toString());
            }
            localStorage.setItem('favTeams', JSON.stringify(favs));
            location.reload();
        }
    })
    .catch(e => console.error('Erro:', e));
};
</script>
```

## 📊 Estrutura do Banco de Dados

### Tabela `favoritos`
```sql
CREATE TABLE favoritos (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,        -- IP ou ID de sessão
    team_id INTEGER NOT NULL,     -- ID do time
    data_criacao TIMESTAMP,        -- Quando foi adicionado
    UNIQUE(user_id, team_id)       -- Evita duplicatas
);
```

### Tabela `historico_pesquisas`
```sql
CREATE TABLE historico_pesquisas (
    id INTEGER PRIMARY KEY,
    user_id TEXT NOT NULL,
    termo TEXT NOT NULL,           -- Termo pesquisado
    data TIMESTAMP                 -- Data da pesquisa
);
```

## 🔒 Considerações de Segurança

⚠️ **Atual**: Usa `request.remote_addr` (IP do cliente)
✅ **Melhor**: Implementar autenticação de usuário

```python
from flask_login import current_user

@app.route('/api/favorito', methods=['POST'])
def api_favorito():
    if not current_user.is_authenticated:
        return jsonify({'erro': 'Não autenticado'}), 401
    
    user_id = current_user.id  # ID único do usuário
    # ... resto do código
```

## 📈 Exemplos de Consulta

### Backup de favoritos
```python
def backup_favoritos(user_id):
    favs = obter_favoritos(user_id)
    with open(f'backup_{user_id}.json', 'w') as f:
        json.dump(favs, f)
```

### Restaurar favoritos
```python
def restaurar_favoritos(user_id, arquivo):
    with open(arquivo) as f:
        favs = json.load(f)
    for team_id in favs:
        adicionar_favorito(user_id, team_id)
```

## 🔄 Sincronização entre Dispositivos

Se implementar autenticação:

```python
# Cliente 1: Adiciona favorito
POST /api/favorito {'team_id': 123, 'action': 'add'}

# Cliente 2: Ao abrir página
GET /api/favoritos -> Retorna todos os favoritos do user_id
```

Ambos os dispositivos verão os mesmos favoritos! ✨

## 🚨 Troubleshooting

### Erro: "database is locked"
→ Aumentar timeout: `conn = sqlite3.connect(DB_PATH, timeout=10)`

### Erro: "table already exists"
→ Normal na primeira execução. `init_db()` verifica com `IF NOT EXISTS`

### Dados não persistem
→ Verificar que `database.py` está sendo importado corretamente

## 📝 Próximos Passos

1. ✅ Implementar autenticação com Flask-Login
2. ✅ Migrar para PostgreSQL para produção
3. ✅ Adicionar API REST completa
4. ✅ Implementar sincronização em tempo real (WebSocket)
