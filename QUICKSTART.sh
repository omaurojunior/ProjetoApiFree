#!/bin/bash
# 🚀 FUTMAX v3.0 - QUICK START GUIDE

echo "================================"
echo "🚀 FUTMAX v3.0 Installation"
echo "================================"
echo ""

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. Verificar Python
echo -e "${BLUE}[1/5]${NC} Verificando Python..."
python --version

# 2. Instalar dependências
echo -e "${BLUE}[2/5]${NC} Instalando dependências..."
pip install -r requirements.txt -q

# 3. Configurar .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}[3/5]${NC} Criando arquivo .env..."
    cat > .env << 'EOF'
FOOTBALL_API_KEY=SUA_CHAVE_AQUI
SECRET_KEY=uma_chave_muito_segura_2026
EOF
    echo "⚠️  Edite o arquivo .env e adicione sua API key!"
else
    echo -e "${GREEN}✓${NC} Arquivo .env existe"
fi

# 4. Informar estrutura
echo -e "${BLUE}[4/5]${NC} Estrutura de arquivos:"
cat << 'EOF'

📦 ProjetoApiFree/
 ├─ 🐍 app.py (Flask + 5 rotas novas)
 ├─ 📋 requirements.txt
 ├─ 📁 static/
 │  ├─ style.css (20+ animações)
 │  ├─ utilities.js (20+ funções)
 │  ├─ manifest.json (PWA)
 │  └─ service-worker.js (Cache)
 ├─ 📁 templates/
 │  ├─ base.html (navbar melhorada)
 │  ├─ comparador.html (NOVO)
 │  ├─ ranking.html (NOVO)
 │  └─ ... outras
 ├─ 📖 FEATURES_V3.md (Documentação)
 ├─ 📖 UTILS_GUIDE.md (Guia de uso)
 └─ 📖 RESUME_V3.md (Resumo visual)

EOF

# 5. Instruções finais
echo -e "${BLUE}[5/5]${NC} Próximos passos:"
cat << 'EOF'

1️⃣  Edite .env com sua API key (football-data.org)

2️⃣  Inicie a aplicação:
    python app.py

3️⃣  Acesse em seu navegador:
    http://localhost:5000

4️⃣  Explore as novas funcionalidades:
    - Navbar > Rankings (Pontos/Gols/Defesa)
    - Navbar > ⚔️ Comparador
    - Teste dark mode 🌙
    - Abra as notificações 🔔

5️⃣  Instale como PWA (celular):
    - Menu (⋮) > Instalar app
    - Funciona offline!

📚 Leia a documentação:
    - FEATURES_V3.md (o que foi adicionado)
    - UTILS_GUIDE.md (como usar as funções)
    - RESUME_V3.md (resumo visual)

🎓 Aprender sobre:
    - APIs REST: /api/favoritos, /api/comparar, /api/ranking
    - Animações: 20+ efeitos CSS prontos
    - PWA: Instalação em celular + offline
    - Service Worker: Cache inteligente

🐛 Se tiver problemas:
    - Verificar console (F12 > Console)
    - Verificar logs em app.log
    - Limpar cache (Ctrl+Shift+Del)

EOF

echo ""
echo -e "${GREEN}================================${NC}"
echo -e "${GREEN}✓ Instalação concluída!${NC}"
echo -e "${GREEN}================================${NC}"
echo ""
echo "Agora execute: python app.py"
