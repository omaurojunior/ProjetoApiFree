import os
import requests
import logging
from functools import wraps
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_caching import Cache
from flask_compress import Compress
# from slowapi iport Limiter
# from slowapi.util import get_remote_address
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

# ===== LOGGING =====
# Configurar logging apenas para console em ambientes serverless (Vercel)
handlers = [logging.StreamHandler()]

# Em desenvolvimento local, também salvar em arquivo
if os.getenv('ENVIRONMENT') != 'production':
    try:
        handlers.append(logging.FileHandler('app.log'))
    except:
        pass  # Se não conseguir criar arquivo, continua sem

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=handlers
)
logger = logging.getLogger(__name__)

# ===== CONFIGURAÇÃO =====
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_key_123')

# Compressão automática de respostas
Compress(app)

# Cache com timeouts diferentes por tipo
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

# Rate limiting
# limiter = Limiter(
#     key_func=get_remote_address,
#     default_limits=["200 per day", "50 per hour"],
#     storage_uri="memory://"
# )
# limiter.init_app(app)

API_KEY = os.getenv('FOOTBALL_API_KEY')
if not API_KEY:
    logger.error("❌ FOOTBALL_API_KEY não configurada no .env")
    
BASE_URL = 'https://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY} if API_KEY else {}

SUPPORTED_LEAGUES = {'BSA': 'Série A'}

# ===== DADOS MANUAIS =====
# Caso a API externa falhe ou para ter informação completa, podemos
# fornecer um dicionário básico dos 20 clubes da Série A. Os dados são
# fictícios/incompletos e servem como fallback.
MANUAL_TEAMS = {
    1: {'id':1,'name':'Flamengo','shortName':'Flamengo','tla':'FLA','crest':'','venue':'Maracanã','founded':1895,'squad':[],
        'phone':'(21) 1234-5678','email':'contato@flamengo.com','address':'Rio de Janeiro, RJ','website':'https://www.flamengo.com.br'},
    2: {'id':2,'name':'Palmeiras','shortName':'Palmeiras','tla':'PAL','crest':'','venue':'Allianz Parque','founded':1914,'squad':[],
        'phone':'(11) 2345-6789','email':'contato@palmeiras.com','address':'São Paulo, SP','website':'https://www.palmeiras.com.br'},
    3: {'id':3,'name':'São Paulo','shortName':'São Paulo','tla':'SPF','crest':'','venue':'Morumbi','founded':1930,'squad':[],
        'phone':'(11) 3456-7890','email':'contato@sampetro.com','address':'São Paulo, SP','website':'https://www.saopaulofc.net'},
    4: {'id':4,'name':'Corinthians','shortName':'Corinthians','tla':'COR','crest':'','venue':'Neo Química Arena','founded':1910,'squad':[],
        'phone':'(11) 4567-8901','email':'contato@corinthians.com','address':'São Paulo, SP','website':'https://www.corinthians.com.br'},
    5: {'id':5,'name':'Grêmio','shortName':'Grêmio','tla':'GRE','crest':'','venue':'Arena do Grêmio','founded':1903,'squad':[],
        'phone':'(51) 5678-9012','email':'contato@gremio.net','address':'Porto Alegre, RS','website':'https://www.gremio.net'},
    6: {'id':6,'name':'Internacional','shortName':'Inter','tla':'INT','crest':'','venue':'Beira-Rio','founded':1909,'squad':[],
        'phone':'(51) 6789-0123','email':'contato@internacional.com','address':'Porto Alegre, RS','website':'https://www.internacional.com.br'},
    7: {'id':7,'name':'Fluminense','shortName':'Fluminense','tla':'FLU','crest':'','venue':'Maracanã','founded':1902,'squad':[],
        'phone':'(21) 7890-1234','email':'contato@fluminense.com','address':'Rio de Janeiro, RJ','website':'https://www.fluminense.com.br'},
    8: {'id':8,'name':'Vasco da Gama','shortName':'Vasco','tla':'VAS','crest':'','venue':'São Januário','founded':1898,'squad':[],
        'phone':'(21) 8901-2345','email':'contato@vasco.com.br','address':'Rio de Janeiro, RJ','website':'https://www.vasco.com.br'},
    9: {'id':9,'name':'Cruzeiro','shortName':'Cruzeiro','tla':'CRU','crest':'','venue':'Mineirão','founded':1921,'squad':[],
        'phone':'(31) 9012-3456','email':'contato@cruzeiro.com.br','address':'Belo Horizonte, MG','website':'https://www.cruzeiro.com.br'},
    10: {'id':10,'name':'Atlético Mineiro','shortName':'Atlético MG','tla':'CAM','crest':'','venue':'Mineirão','founded':1908,'squad':[],
        'phone':'(31) 0123-4567','email':'contato@atleticomg.com.br','address':'Belo Horizonte, MG','website':'https://www.atletico.com.br'},
    11: {'id':11,'name':'Athletico Paranaense','shortName':'Athletico PR','tla':'CAP','crest':'','venue':'Arena da Baixada','founded':1924,'squad':[],
        'phone':'(41) 1234-5678','email':'contato@athletico.com.br','address':'Curitiba, PR','website':'https://www.athletico.com.br'},
    12: {'id':12,'name':'Coritiba','shortName':'Coritiba','tla':'CFC','crest':'','venue':'Couto Pereira','founded':1909,'squad':[],
        'phone':'(41) 2345-6789','email':'contato@coritiba.com.br','address':'Curitiba, PR','website':'https://www.coritiba.com.br'},
    13: {'id':13,'name':'Santos','shortName':'Santos','tla':'SAN','crest':'','venue':'Vila Belmiro','founded':1912,'squad':[],
        'phone':'(13) 3456-7890','email':'contato@santosfc.com.br','address':'Santos, SP','website':'https://www.santosfc.com.br'},
    14: {'id':14,'name':'Ponte Preta','shortName':'Ponte Preta','tla':'PON','crest':'','venue':'Moisés Lucarelli','founded':1900,'squad':[],
        'phone':'(19) 4567-8901','email':'contato@pontepreta.com.br','address':'Campinas, SP','website':'https://www.pontepreta.com.br'},
    15: {'id':15,'name':'Guarani','shortName':'Guarani','tla':'GUA','crest':'','venue':'Brinco de Ouro','founded':1911,'squad':[],
        'phone':'(19) 5678-9012','email':'contato@guarani.com.br','address':'Campinas, SP','website':'https://www.guaranifc.com.br'},
    16: {'id':16,'name':'Bahia','shortName':'Bahia','tla':'BHA','crest':'','venue':'Fonte Nova','founded':1931,'squad':[],
        'phone':'(71) 6789-0123','email':'contato@ecbahia.com.br','address':'Salvador, BA','website':'https://www.esporteclubebahia.com.br'},
    17: {'id':17,'name':'Vitória','shortName':'Vitória','tla':'VIT','crest':'','venue':'Barradão','founded':1902,'squad':[],
        'phone':'(71) 7890-1234','email':'contato@ecvitoria.com.br','address':'Salvador, BA','website':'https://www.ecvitoria.com.br'},
    18: {'id':18,'name':'Internacional (SP)','shortName':'Inter SP','tla':'INT','crest':'','venue':'Moisés Lucarelli','founded':1928,'squad':[],
        'phone':'(11) 8901-2345','email':'contato@intersp.com.br','address':'São Paulo, SP','website':'https://www.intersp.com.br'},
    19: {'id':19,'name':'Náutico','shortName':'Náutico','tla':'NAU','crest':'','venue':'Ilha do Retiro','founded':1901,'squad':[],
        'phone':'(81) 9012-3456','email':'contato@nautico.com.br','address':'Recife, PE','website':'https://www.nautico-pe.com.br'},
    20: {'id':20,'name':'Sport','shortName':'Sport','tla':'SPT','crest':'','venue':'Ilha do Retiro','founded':1905,'squad':[],
        'phone':'(81) 0123-4567','email':'contato@sportrecife.com.br','address':'Recife, PE','website':'https://www.sportrecife.com.br'}
}

# ===== DECORATORS =====
def validate_league(f):
    """Valida se a liga é suportada."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        league = request.args.get('league', 'BSA')
        if league not in SUPPORTED_LEAGUES:
            flash(f"❌ Liga '{league}' não suportada", "danger")
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def handle_api_error(f):
    """Decorator para tratamento robusto de erros da API."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except requests.exceptions.Timeout:
            logger.error("Timeout na API")
            flash("⏱️ A API demorou muito. Tente novamente.", "danger")
            return redirect(url_for('index'))
        except requests.exceptions.HTTPError as e:
            logger.error(f"erro HTTP: {e}")
            if e.response.status_code == 404:
                flash("❌ Recurso não encontrado", "danger")
            elif e.response.status_code == 429:
                flash("⚠️ Limite de requisições atingido. Tente mais tarde.", "warning")
            else:
                flash(f"❌ Erro na API (código {e.response.status_code})", "danger")
            return redirect(url_for('index'))
        except Exception as e:
            logger.exception(f"Erro inesperado: {e}")
            flash("❌ Erro inesperado. Contate o suporte.", "danger")
            return redirect(url_for('index'))
    return decorated_function

# ===== API HELPERS =====
def get_api_data(endpoint, timeout=10):
    """Busca dados da API com tratamento de erros."""
    if not API_KEY:
        logger.error("API key não configurada")
        return None
        
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        response.raise_for_status()
        logger.info(f"✅ API Call: {endpoint}")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao chamar {endpoint}: {e}")
        return None

@app.route('/')
# @limiter.limit("30 per minute")
@handle_api_error
@validate_league
def index():
    league_id = request.args.get('league', 'BSA')
    rodada_selecionada = request.args.get('matchday', type=int)
    
    data = get_api_data(f"competitions/{league_id}/matches")
    if not data:
        flash("❌ Não foi possível carregar os dados das partidas", "danger")
        return render_template('index.html', matches=[], rodada_atual=1)

    if rodada_selecionada is None:
        rodada_selecionada = data.get('resultSet', {}).get('currentMatchday', 1)
    
    # Validar rodada
    if rodada_selecionada < 1 or rodada_selecionada > 38:
        rodada_selecionada = 1
        
    matches = [m for m in data.get('matches', []) if m.get('matchday') == rodada_selecionada]
    
    return render_template('index.html', 
                           matches=matches, 
                           rodada_atual=rodada_selecionada, 
                           total_rodadas=38)

@app.route('/confronto/<int:match_id>')
# @limiter.limit("30 per minute")
@handle_api_error
def confronto_direto(match_id):
    # Validar match_id
    if match_id <= 0:
        flash("❌ ID de partida inválido", "danger")
        return redirect(url_for('index'))
        
    data = get_api_data(f"matches/{match_id}")
    if not data:
        flash("❌ Partida não encontrada", "danger")
        return redirect(url_for('index'))

    partida = data.get('match') if 'match' in data else data
    h2h = data.get('head2head')

    return render_template('confronto.html', 
                           partida=partida, 
                           h2h=h2h)

@app.route('/ligas')
# @limiter.limit("30 per minute")
@handle_api_error
@validate_league
def ligas():
    league_id = request.args.get('league', 'BSA')
    data = get_api_data(f"competitions/{league_id}/standings")
    try:
        standings = data.get('standings', [{}])[0].get('table', []) if data else []
    except (IndexError, KeyError, TypeError):
        standings = []
    return render_template('ligas.html', standings=standings, league_id=league_id, leagues=SUPPORTED_LEAGUES)

@app.route('/artilharia')
# @limiter.limit("30 per minute")
@handle_api_error
@validate_league
def artilharia():
    league_id = request.args.get('league', 'BSA')
    data = get_api_data(f"competitions/{league_id}/scorers")
    scorers = data.get('scorers', []) if data else []
    return render_template('artilharia.html', scorers=scorers, league_id=league_id, leagues=SUPPORTED_LEAGUES)

@app.template_filter('format_date')
def format_date(value):
    """Formata data ISO para formato brasileiro."""
    if not value:
        return ""
    try:
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('%d/%m %H:%M')
    except Exception as e:
        logger.debug(f"Erro ao formatar data: {e}")
        return value

@app.route('/pesquisa', methods=['GET', 'POST'])
# @limiter.limit("30 per minute")
@handle_api_error
def pesquisa():
    teams = []
    query = ""

    # aceitar também GET para facilitar sugestões via JS
    if request.method == 'POST':
        query = request.form.get('nome_time', '').strip()
    else:
        query = request.args.get('nome_time', '').strip()

    if query:
        # validações
        if len(query) < 2:
            flash("❌ Digite no mínimo 2 caracteres", "warning")
            return render_template('pesquisa.html', teams=[], query=query)
        if len(query) > 50:
            flash("❌ Máximo 50 caracteres", "warning")
            return render_template('pesquisa.html', teams=[], query=query)

        query_lower = query.lower()
        for lid in SUPPORTED_LEAGUES.keys():
            data = get_api_data(f"competitions/{lid}/teams")
            if data and 'teams' in data:
                found = [t for t in data['teams']
                        if query_lower in t.get('name', '').lower()
                        or query_lower in t.get('shortName', '').lower()]
                teams.extend(found)

        teams = list({v['id']: v for v in teams}.values())
        if not teams:
            flash(f"ℹ️ Nenhum time encontrado para '{query}'", "info")
    else:
        # sem query lista todos os times para navegação
        for lid in SUPPORTED_LEAGUES.keys():
            data = get_api_data(f"competitions/{lid}/teams")
            if data and 'teams' in data:
                teams.extend(data['teams'])
        teams = list({v['id']: v for v in teams}.values())

    return render_template('pesquisa.html', teams=teams, query=query)

@app.route('/time/<int:team_id>')
@cache.cached(timeout=3600)
@handle_api_error
def detalhes_time(team_id):
    # Validar team_id
    if team_id <= 0:
        flash("❌ ID de time inválido", "danger")
        return redirect(url_for('pesquisa'))
        
    team = get_api_data(f"teams/{team_id}")
    if not team:
        flash("❌ Time não encontrado", "danger")
        return redirect(url_for('pesquisa'))
    
    squad_list = team.get('squad', [])
    squad = {
        'Goleiros': [p for p in squad_list if p.get('position') == 'Goalkeeper'],
        'Defensores': [p for p in squad_list if p.get('position') == 'Defence'],
        'Meias': [p for p in squad_list if p.get('position') == 'Midfield'],
        'Atacantes': [p for p in squad_list if p.get('position') == 'Offence'],
    }

    # calcular estatísticas do elenco
    today = datetime.utcnow().date()
    ages = []
    nationality_counts = {}
    for p in squad_list:
        dob = p.get('dateOfBirth')
        nat = p.get('nationality')
        if dob:
            try:
                d = datetime.strptime(dob, '%Y-%m-%d').date()
                age = today.year - d.year - ((today.month, today.day) < (d.month, d.day))
                ages.append(age)
            except:
                pass
        if nat:
            nationality_counts[nat] = nationality_counts.get(nat, 0) + 1
    stats = {}
    if ages:
        stats['min_age'] = min(ages)
        stats['max_age'] = max(ages)
        stats['avg_age'] = sum(ages) // len(ages)
    stats['nationalities'] = nationality_counts

    competitions = team.get('runningCompetitions', [])
    return render_template('time.html', team=team, squad=squad, competitions=competitions, stats=stats)

# ===== API REST ENDPOINTS =====
@app.route('/api/favoritos', methods=['GET', 'POST', 'DELETE'])
# @limiter.limit("60 per minute")
def api_favoritos():
    """API RESTful para gerenciar favoritos."""
    user_id = request.remote_addr
    
    if request.method == 'POST':
        data = request.get_json()
        team_id = data.get('team_id')
        
        if not team_id or team_id <= 0:
            return jsonify({'erro': 'team_id inválido'}), 400
        
        logger.info(f"⭐ Favorito adicionado: {team_id}")
        return jsonify({'sucesso': True, 'mensagem': 'Adicionado aos favoritos'})
    
    elif request.method == 'DELETE':
        data = request.get_json()
        team_id = data.get('team_id')
        
        logger.info(f"✓ Favorito removido: {team_id}")
        return jsonify({'sucesso': True, 'mensagem': 'Removido dos favoritos'})
    
    return jsonify({'favoritos': []})

@app.route('/api/comparar', methods=['POST'])
# @limiter.limit("30 per minute")
@handle_api_error
def api_comparar():
    """Compara estatísticas entre dois times.

    Retorna um JSON com informações básicas e adicionais sobre cada
    equipe. Caso a API retorne menos campos, usamos defaults para evitar
    quebra na interface front-end.
    """
    data = request.get_json()
    team1_id = data.get('team1_id')
    team2_id = data.get('team2_id')
    
    if not team1_id or not team2_id:
        return jsonify({'erro': 'IDs dos times são obrigatórios'}), 400
    
    team1 = get_api_data(f"teams/{team1_id}")
    team2 = get_api_data(f"teams/{team2_id}")
    
    if not team1 or not team2:
        return jsonify({'erro': 'Time(s) não encontrado(s)'}), 404
    
    def summarize(team):
        return {
            'id': team.get('id'),
            'nome': team.get('name'),
            'escudo': team.get('crest'),
            'fundacao': team.get('founded'),
            'jogadores': len(team.get('squad', [])),
            'estadio': team.get('venue'),
            'tla': team.get('tla'),
            'shortName': team.get('shortName'),
            'phone': team.get('phone'),
            'email': team.get('email'),
            'endereco': team.get('address'),
            'website': team.get('website')
        }
    
    comparacao = {
        'time1': summarize(team1),
        'time2': summarize(team2)
    }
    
    logger.info(f"📊 Comparação: {team1_id} vs {team2_id}")
    return jsonify(comparacao)


@app.route('/api/teams', methods=['GET'])
@cache.cached(timeout=600, query_string=True)
@handle_api_error
def api_teams():
    """Busca times pelo nome (case‑insensitive) em todas as ligas suportadas.

    Usa o mesmo cache do Flask-Caching para não sobrecarregar a API externa.
    """
    q = request.args.get('q', '').strip().lower()
    if not q:
        # sem termo, devolver todos os manuais (poucos) e possivelmente dados da API
        results = []
        for t in MANUAL_TEAMS.values():
            results.append({
                'id': t['id'],
                'name': t['name'],
                'shortName': t.get('shortName'),
                'crest': t.get('crest','')
            })
        return jsonify(results)

    results = []
    # primeiro, buscar na API externa
    for lid in SUPPORTED_LEAGUES.keys():
        data = get_api_data(f"competitions/{lid}/teams")
        if data and 'teams' in data:
            for t in data['teams']:
                name = t.get('name', '').lower()
                short = t.get('shortName', '').lower()
                if q in name or q in short:
                    results.append({
                        'id': t.get('id'),
                        'name': t.get('name'),
                        'shortName': t.get('shortName'),
                        'crest': t.get('crest'),
                    })
    # adicionar matches do manual se não houver match API
    for tid, t in MANUAL_TEAMS.items():
        if q in t.get('name','').lower() or q in t.get('shortName','').lower():
            results.append({
                'id': t['id'],
                'name': t['name'],
                'shortName': t.get('shortName'),
                'crest': t.get('crest','')
            })
    # remover duplicatas por id
    seen = set()
    unique = []
    for t in results:
        if t['id'] not in seen:
            seen.add(t['id'])
            unique.append(t)
    return jsonify(unique)


@app.route('/api/team/<int:team_id>', methods=['GET'])
@cache.cached(timeout=3600)
@handle_api_error
def api_team(team_id):
    """Retorna os dados brutos de um time em JSON. Usa fallback manual se API falhar."""
    data = get_api_data(f"teams/{team_id}")
    if not data:
        # verificar fallback manual
        manual = MANUAL_TEAMS.get(team_id)
        if manual:
            return jsonify(manual)
        return jsonify({'erro': 'Time não encontrado'}), 404
    return jsonify(data)



@app.route('/api/head2head', methods=['GET'])
@cache.cached(timeout=600, query_string=True)
@handle_api_error
def api_head2head():
    """Retorna últimos confrontos entre dois times.

    Se não houver dados na API, retorna lista vazia. Filtra partidas
    já finalizadas onde os dois times se enfrentaram.
    """
    t1 = request.args.get('team1', type=int)
    t2 = request.args.get('team2', type=int)
    if not t1 or not t2:
        return jsonify([])
    # buscar partidas do primeiro time e filtrar pelo segundo
    data = get_api_data(f"teams/{t1}/matches?status=FINISHED&limit=20")
    matches = []
    if data and 'matches' in data:
        for m in data['matches']:
            home = m.get('homeTeam', {}).get('id')
            away = m.get('awayTeam', {}).get('id')
            if home == t2 or away == t2:
                matches.append({
                    'utcDate': m.get('utcDate'),
                    'homeTeam': m.get('homeTeam', {}).get('name'),
                    'awayTeam': m.get('awayTeam', {}).get('name'),
                    'score': m.get('score', {}).get('fullTime')
                })
    return jsonify(matches)


@app.route('/api/ranking', methods=['GET'])
@cache.cached(timeout=1800)
# @limiter.limit("50 per minute")
@handle_api_error
def api_ranking():
    """Retorna ranking de times por vitórias, gols, etc."""
    league_id = request.args.get('league', 'BSA')
    tipo = request.args.get('tipo', 'pontos')
    
    data = get_api_data(f"competitions/{league_id}/standings")
    if not data:
        return jsonify({'erro': 'Não foi possível carregar ranking'}), 500
    
    try:
        table = data.get('standings', [{}])[0].get('table', [])
        
        if tipo == 'gols':
            table_sorted = sorted(table, key=lambda x: x.get('goalsFor', 0), reverse=True)
        elif tipo == 'defesa':
            table_sorted = sorted(table, key=lambda x: x.get('goalsAgainst', 0))
        else:
            table_sorted = table
        
        ranking = [
            {
                'posicao': i + 1,
                'time': t.get('team', {}).get('name'),
                'escudo': t.get('team', {}).get('crest'),
                'pontos': t.get('points'),
                'jogos': t.get('playedGames'),
                'gols_favor': t.get('goalsFor'),
                'gols_contra': t.get('goalsAgainst'),
                'saldo': t.get('goalDifference')
            }
            for i, t in enumerate(table_sorted[:20])
        ]
        
        logger.info(f"📈 Ranking gerado: {tipo}")
        return jsonify(ranking)
    
    except (IndexError, KeyError, TypeError) as e:
        logger.error(f"Erro ao processar ranking: {e}")
        return jsonify({'erro': 'Erro ao processar dados'}), 500

@app.route('/favoritos')
# @limiter.limit("30 per minute")
@handle_api_error
def favoritos():
    """Página de favoritos (gerenciados via localStorage)."""
    return render_template('favoritos.html')


@app.route('/comparador')
# @limiter.limit("30 per minute")
def comparador():
    """Página para comparar dois times lado a lado."""
    return render_template('comparador.html')

@app.route('/ranking/<tipo>')
# @limiter.limit("30 per minute")
@handle_api_error
@validate_league
def ranking_times(tipo):
    """Ranking de times por categoria."""
    league_id = request.args.get('league', 'BSA')
    
    if tipo not in ['pontos', 'gols', 'defesa']:
        flash("❌ Tipo de ranking inválido", "danger")
        return redirect(url_for('ligas'))
    
    data = get_api_data(f"competitions/{league_id}/standings")
    if not data:
        flash("❌ Não foi possível carregar ranking", "danger")
        return redirect(url_for('ligas'))
    
    try:
        table = data.get('standings', [{}])[0].get('table', [])
        
        if tipo == 'gols':
            standings = sorted(table, key=lambda x: x.get('goalsFor', 0), reverse=True)
            titulo = "🎯 Ranking por Gols"
        elif tipo == 'defesa':
            standings = sorted(table, key=lambda x: x.get('goalsAgainst', 0))
            titulo = "🛡️ Ranking por Defesa"
        else:
            standings = table
            titulo = "📊 Ranking por Pontos"
        
        return render_template('ranking.html', 
                             standings=standings, 
                             tipo=tipo, 
                             titulo=titulo,
                             league_id=league_id,
                             leagues=SUPPORTED_LEAGUES)
    
    except (IndexError, KeyError, TypeError):
        standings = []
        titulo = "Ranking"
        return render_template('ranking.html', 
                             standings=standings, 
                             tipo=tipo, 
                             titulo=titulo)

# ===== ERROR HANDLERS =====
@app.errorhandler(429)
def ratelimit_handler(e):
    """Handler para rate limit."""
    flash("⚠️ Muitas requisições. Aguarde um tempo.", "warning")
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    """Handler para página não encontrada."""
    logger.warning(f"404: {request.path}")
    return render_template('index.html', matches=[], rodada_atual=1), 404

@app.errorhandler(500)
def server_error(e):
    """Handler para erro interno."""
    logger.exception("Erro interno do servidor")
    flash("❌ Erro interno do servidor", "danger")
    return redirect(url_for('index')), 500