import os
import requests
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_caching import Cache
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev_key_123')

cache = Cache(config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})
cache.init_app(app)

API_KEY = os.getenv('FOOTBALL_API_KEY')
BASE_URL = 'https://api.football-data.org/v4'
HEADERS = {'X-Auth-Token': API_KEY}

SUPPORTED_LEAGUES = {'BSA': 'Série A'}

def get_api_data(endpoint):
    url = f"{BASE_URL}/{endpoint}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Erro na API: {e}")
        return None

@app.template_filter('format_date')
def format_date(value):
    if not value: return ""
    try:
        dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return dt.strftime('%d/%m %H:%M')
    except: return value

@app.route('/')
def index():
    league_id = request.args.get('league', 'BSA')
    # Corrigido para matchday para bater com o HTML
    rodada_selecionada = request.args.get('matchday', type=int)
    
    data = get_api_data(f"competitions/{league_id}/matches")
    if not data: return "Erro ao carregar dados", 500

    if rodada_selecionada is None:
        rodada_selecionada = data.get('resultSet', {}).get('currentMatchday', 1)

    matches = [m for m in data.get('matches', []) if m.get('matchday') == rodada_selecionada]
    
    return render_template('index.html', 
                           matches=matches, 
                           rodada_atual=rodada_selecionada, 
                           total_rodadas=38)

@app.route('/confronto/<int:match_id>')
def confronto_direto(match_id):
    data = get_api_data(f"matches/{match_id}")
    
    if not data:
        flash("Não foi possível carregar os dados da partida.")
        return redirect(url_for('index'))

    # A API retorna o jogo dentro da chave 'match' ou no objeto principal
    partida = data.get('match') if 'match' in data else data
    h2h = data.get('head2head')

    # DEBUG: Remova isso depois de testar
    # print(f"Dados H2H: {h2h}") 

    return render_template('confronto.html', 
                           partida=partida, 
                           h2h=h2h)
@app.route('/ligas')
def ligas():
    league_id = request.args.get('league', 'BSA')
    data = get_api_data(f"competitions/{league_id}/standings")
    try:
        standings = data.get('standings', [{}])[0].get('table', [])
    except:
        standings = []
    return render_template('ligas.html', standings=standings, league_id=league_id, leagues=SUPPORTED_LEAGUES)

@app.route('/artilharia')
def artilharia():
    league_id = request.args.get('league', 'BSA')
    data = get_api_data(f"competitions/{league_id}/scorers")
    scorers = data.get('scorers', []) if data else []
    return render_template('artilharia.html', scorers=scorers, league_id=league_id, leagues=SUPPORTED_LEAGUES)

@app.route('/pesquisa', methods=['GET', 'POST'])
def pesquisa():
    teams = []
    query = ""
    if request.method == 'POST':
        query = request.form.get('nome_time', '').lower()
        for lid in SUPPORTED_LEAGUES.keys():
            data = get_api_data(f"competitions/{lid}/teams")
            if data and 'teams' in data:
                found = [t for t in data['teams'] if query in t['name'].lower() or query in t['shortName'].lower()]
                teams.extend(found)
        # Remove duplicatas
        teams = {v['id']: v for v in teams}.values()
        
    return render_template('pesquisa.html', teams=teams, query=query)

@app.route('/time/<int:team_id>')
@cache.cached(timeout=3600)
def detalhes_time(team_id):
    team = get_api_data(f"teams/{team_id}")
    if not team: return "Erro ao buscar time", 404
    
    squad = {
        'Goleiros': [p for p in team.get('squad', []) if p['position'] == 'Goalkeeper'],
        'Defensores': [p for p in team.get('squad', []) if p['position'] == 'Defence'],
        'Meias': [p for p in team.get('squad', []) if p['position'] == 'Midfield'],
        'Atacantes': [p for p in team.get('squad', []) if p['position'] == 'Offence'],
    }

    running_competitions = team.get('runningCompetitions', [])
    return render_template('time.html', team=team, squad=squad, competitions=running_competitions)

if __name__ == '__main__':
    app.run(debug=True)