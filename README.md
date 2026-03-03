# ⚽ FUTMAX - API de Futebol Brasileiro

Sistema web para consultar informações sobre futebol brasileiro usando a API [football-data.org](https://www.football-data.org).

## 🎯 Funcionalidades

- 📊 **Resultados e Rodadas**: Visualize todas as partidas da Série A por rodada
- 🏆 **Classificação**: Tabela atualizada com pontos, vitórias, derrotas
- 🎯 **Artilharia**: Rankings de maiores goleadores
- 🔍 **Busca de Times**: Pesquise times e veja detalhes do elenco
- ⭐ **Favoritos**: Salve seus times preferidos (localStorage)
- 📈 **H2H**: Compare histórico direto entre times
- 🌙 **Modo Escuro**: Interface adaptativa

## 🚀 Como Instalar

### Pré-requisitos
- Python 3.8+
- pip

### Passos

1. **Clonar/Baixar projeto**
```bash
cd ProjetoApiFree
```

2. **Criar ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. **Instalar dependências**
```bash
pip install -r requirements.txt
```

4. **Configurar variáveis de ambiente**
```bash
# Crie arquivo .env no raiz do projeto
FOOTBALL_API_KEY=sua_chave_aqui
SECRET_KEY=uma_chave_muito_segura_e_longa
```

5. **Gerar chave da API**
- Acesse https://www.football-data.org
- Faça login e vá em "My Account"
- Copie seu API Token

6. **Executar aplicação**
```bash
python app.py
```

7. **Acessar em seu navegador**
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
ProjetoApiFree/
├── app.py                 # Aplicação principal Flask
├── database.py           # Sistema de persistência (opcional)
├── requirements.txt      # Dependências
├── .env                  # Variáveis de ambiente (NÃO COMMITAR!)
├── .gitignore           # Arquivos ignorados no Git
├── vercel.json          # Config para deploy no Vercel
├── static/
│   └── style.css        # Estilos CSS
├── templates/
│   ├── base.html        # Template base
│   ├── index.html       # Página de resultados
│   ├── ligas.html       # Classificação
│   ├── artilharia.html  # Rankings de gols
│   ├── pesquisa.html    # Busca de times
│   ├── time.html        # Detalhes do time
│   └── confronto.html   # H2H entre times
├── MELHORIAS.md         # Resumo de melhorias v2.0
├── DATABASE_GUIDE.md    # Guia de banco de dados
└── README.md            # Este arquivo
```

## 🔐 Segurança

### ⚠️ CRÍTICO
Seu arquivo `.env` **NÃO deve ser commitado** no Git e contém:
- API Key (autenticação)
- Secret Key (sessão)

O arquivo está no `.gitignore`. Se já foi exposto:
1. Revogue a chave em football-data.org
2. Gere uma nova chave
3. Atualize `.env`

## 📚 Documentação das Rotas

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Página inicial com resultados |
| `/ligas` | GET | Tabela de classificação |
| `/artilharia` | GET | Rankings de artilheiros |
| `/pesquisa` | GET/POST | Buscar times |
| `/time/<id>` | GET | Detalhes do time |
| `/confronto/<id>` | GET | H2H entre times |

### Parâmetros

**Rodada**:
```
/?matchday=10  -> 10ª rodada
```

**Liga** (futura expansão):
```
/?league=BSA   -> Série A (padrão)
```

## 🎨 Tecnologias

### Backend
- **Flask** 3.1.2 - Framework web
- **Requests** 2.32.5 - HTTP client
- **Flask-Caching** 2.3.1 - Cache
- **Flask-Compress** 1.15 - Compressão GZIP
- **slowapi** 0.1.9 - Rate limiting
- **python-dotenv** 1.1.0 - Variáveis de ambiente

### Frontend
- **Bootstrap** 5.3.0 - CSS framework
- **Chart.js** - Gráficos
- **Font Awesome** 6.0 - Ícones
- **Poppins Font** - Tipografia

## ⚡ Performance

| Métrica | Valor |
|---------|-------|
| Compressão | -70% (GZIP) |
| Cache TTL | 5 min (padrão) |
| Rate Limit | 200 req/dia, 50/hora |
| Timeout API | 10 segundos |

## 🌐 Deploy

### Vercel
```bash
# Arquivo vercel.json já está configurado
vercel deploy
```

### Heroku
```bash
# 1. Criar app
heroku create seu-app-name

# 2. Definir variáveis
heroku config:set FOOTBALL_API_KEY=sua_chave
heroku config:set SECRET_KEY=sua_chave_secreta

# 3. Deploy
git push heroku main
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🐛 Troubleshooting

### "API key not found"
→ Verifique se `.env` existe e tem `FOOTBALL_API_KEY=...`

### "Connection timeout"
→ Verifique internet, pode estar sem acesso à football-data.org

### "Rate limit exceeded"
→ Aguarde 1 hora ou solicite plano premium em football-data.org

### Modo escuro não funciona
→ Limpe cache do navegador: Ctrl+Shift+Del

## 📊 Melhorias Implementadas v2.0

✅ Logging estruturado
✅ Compressão GZIP automática
✅ Rate limiting por IP
✅ Tratamento robusto de erros
✅ Validação de entrada
✅ Status visual para partidas AO VIVO
✅ Histórico de pesquisas
✅ Sistema de persistência (database.py)
✅ Documentação completa

Ver [MELHORIAS.md](MELHORIAS.md) para detalhes.

## 📝 Licença

Projeto educacional - Use livremente.

## 👨‍💻 Autor

Desenvolvido como projeto de Backend 2 - SENAI 2026

## 🤝 Contribuições

Pull requests são bem-vindos! Para mudanças grandes, abra uma issue primeiro.

## 📞 Suporte

- 📧 Email de suporte: [seu-email@example.com]
- 🐛 Reporte bugs em: [Issues]
- 💬 Discussões: [Discussions]

---

**Última atualização**: 3 de março de 2026
**Versão**: 2.0
**Status**: ✅ Pronto para produção
