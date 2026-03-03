# 🎓 Boas Práticas de Desenvolvimento - FUTMAX

## 📋 Padrões de Código

### 1. Estrutura de Função
```python
@app.route('/rota')
@limiter.limit("30 per minute")  # Rate limiting
@handle_api_error                 # Tratamento de erro
def minha_funcao():
    """Descrição breve da função."""
    # Validação de entrada
    if not dados:
        flash("❌ Validação falhou", "danger")
        return redirect(url_for('index'))
    
    # Lógica principal
    resultado = get_api_data(f"endpoint")
    
    # Tratamento nulo
    if not resultado:
        logger.warning("Dados nulos")
        return render_template('erro.html')
    
    # Retornar template
    return render_template('template.html', dados=resultado)
```

### 2. Tratamento de Erros
```python
# ❌ NÃO FAÇA
try:
    dados = get_api_data("endpoint")
except:
    return "Erro", 500

# ✅ FAÇA ASSIM
try:
    dados = get_api_data("endpoint")
except requests.exceptions.Timeout:
    logger.error("Timeout na API")
    flash("⏱️ Tempo limite excedido", "warning")
    return redirect(url_for('index'))
except requests.exceptions.HTTPError as e:
    logger.error(f"HTTP {e.response.status_code}")
    # Tratar por código específico
except Exception as e:
    logger.exception(f"Erro inesperado: {e}")
    flash("❌ Erro interno", "danger")
    return redirect(url_for('index'))
```

### 3. Logging
```python
# Informação
logger.info("✅ Dados carregados com sucesso")

# Debug (detalhes é muito)
logger.debug(f"Dados recebidos: {dados}")

# Aviso (algo anormal)
logger.warning("⚠️ API respondeu lentamente")

# Erro
logger.error("❌ Falha ao conectar")

# Excepção com traceback
logger.exception("Erro crítico:")
```

### 4. Validação
```python
# ✅ Sempre validar entrada do usuário
@app.route('/usuario/<int:user_id>')
def perfil_usuario(user_id):
    # Validar tipo
    if not isinstance(user_id, int):
        return redirect(url_for('index'))
    
    # Validar range
    if user_id <= 0 or user_id > 999999:
        flash("ID inválido", "danger")
        return redirect(url_for('index'))
    
    # Validar existência
    usuario = buscar_usuario(user_id)
    if not usuario:
        flash("Usuário não encontrado", "danger")
        return redirect(url_for('index'))
    
    return render_template('perfil.html', usuario=usuario)
```

## 🎨 Padrões de Frontend

### 1. Mensagens Flash
```html
<!-- No template base -->
{% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
        {% for category, message in messages %}
        <div class="alert alert-{{ category }}">
            {{ message }}
        </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

### 2. Ícones e Emojis
```
✅ Sucesso
❌ Erro
⚠️ Aviso
ℹ️ Informação
⏰ Tempo/Agendado
🔴 AO VIVO
⏸️ Pausado
🎯 Alvo/Meta
📊 Dados/Estatística
🔍 Busca
⭐ Favorito
🌙 Modo Escuro
```

### 3. CSS Classes
```css
/* Uso de variáveis */
color: var(--br-verde);

/* BEM (Block Element Modifier) */
.card-jogo { }
.card-jogo__header { }
.card-jogo--active { }

/* Responsive */
@media (max-width: 768px) {
    .hidden-mobile { display: none; }
}
```

## 🔐 Checklist de Segurança

### Antes de fazer Push
- [ ] Nenhum `.env` commitado
- [ ] Nenhuma API key em comments
- [ ] Validação de entrada em TODAS as rotas
- [ ] Tratamento de erro em TODAS as requisições
- [ ] CSRF token em formulários (Flask faz automaticamente)
- [ ] Sem `eval()` ou `exec()`
- [ ] SQL Injection proteção (usar parameterizado)

### Antes de Deploy
- [ ] `DEBUG = False`
- [ ] `SECRET_KEY` forte e aleatória
- [ ] HTTPS ativado
- [ ] Rate limiting ativo
- [ ] Logs sendo salvos
- [ ] Variáveis de ambiente configuradas
- [ ] Backup do banco de dados

## 📦 Gerenciamento de Dependências

### Atualizar requirements.txt
```bash
# Verificar versões desatualizadas
pip list --outdated

# Atualizar tudo
pip install --upgrade pip
pip install -r requirements.txt --upgrade

# Gerar novo requirements.txt
pip freeze > requirements.txt
```

### Adicionar nova dependência
```bash
# Instalar
pip install novo-pacote==1.0.0

# Adicionar a requirements.txt
pip freeze | grep novo-pacote >> requirements.txt
```

## 🧪 Testes

### Exemplo de Teste Unitário
```python
import unittest
from app import app

class TestRotas(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_status_200(self):
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, 200)
    
    def test_index_contem_rodada(self):
        resp = self.app.get('/')
        self.assertIn(b'RODADA', resp.data)
    
    def test_pesquisa_invalida(self):
        resp = self.app.post('/pesquisa', data={'nome_time': 'a'})
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'mínimo 2', resp.data)

if __name__ == '__main__':
    unittest.main()
```

## 📈 Performance

### Cache
```python
# Cache por 1 hora
@app.route('/dados')
@cache.cached(timeout=3600)
def dados():
    return get_api_data("...")

# Cache por 5 minutos (padrão)
@app.route('/resultados')
@cache.cached()
def resultados():
    return ...

# Sem cache
@app.route('/ao-vivo')
def ao_vivo():
    return get_api_data("...")  # Sempre fresco
```

### Otimização de Query
```python
# ❌ N+1 Query Problem
for time in times:
    detalhes = get_api_data(f"teams/{time.id}")

# ✅ Melhor
times_com_detalhes = [
    {**time, 'detalhes': get_api_data(f"teams/{time['id']}")}
    for time in times
]
```

## 🚀 Deployment Checklist

### Antes de Deploy
- [ ] Todos os testes passando
- [ ] Sem warnings/erros no log
- [ ] Dependências atualizadas
- [ ] `.env` configurado no servidor
- [ ] Certificado SSL válido
- [ ] Backup automático ativo

### Pós Deploy
- [ ] Verificar logs
- [ ] Testar todas as rotas
- [ ] Verificar cache
- [ ] Monitorar performance
- [ ] Verificar erros 404/500

## 📝 Convenções de Nomenclatura

```python
# Variáveis
user_id = 123              # snake_case
usuarios = []              # Plural para listas

# Funções
def get_usuario(id):       # snake_case
def is_valido():           # is_ para booleanos
def set_nome(nome):        # set_ para setters

# Classes
class UsuarioManager:      # PascalCase
class APIError(Exception): # Exceção também PascalCase

# Constantes
API_KEY = "..."            # UPPER_CASE
MAX_TENTATIVAS = 3         # UPPER_CASE
```

## 🔄 Fluxo de Desenvolvimento

```
1. Crie issue/feature (descreva o que vai fazer)
2. Crie branch (git checkout -b feature/nome)
3. Desenvolva + commit frequentes
4. Testes passando
5. Pull request com descrição
6. Code review
7. Merge em main
8. Deploy com tag de versão
```

## 📚 Referências

- [Flask Docs](https://flask.palletsprojects.com/)
- [Football-Data API](https://www.football-data.org/documentation)
- [PEP 8 - Style Guide](https://pep8.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Última atualização**: 3 de março de 2026
