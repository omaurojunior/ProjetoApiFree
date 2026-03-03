"""
Sistema de persistência de favoritos em banco de dados SQLite.
Sincroniza favoritos entre múltiplos dispositivos/navegadores.
"""

import sqlite3
import logging
from datetime import datetime
from contextlib import contextmanager

logger = logging.getLogger(__name__)

DB_PATH = 'favoritos.db'

def init_db():
    """Inicializa banco de dados com tabelas necessárias."""
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS favoritos (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                team_id INTEGER NOT NULL,
                data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(user_id, team_id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS historico_pesquisas (
                id INTEGER PRIMARY KEY,
                user_id TEXT NOT NULL,
                termo TEXT NOT NULL,
                data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        logger.info("✅ Banco de dados inicializado")

@contextmanager
def get_connection():
    """Context manager para conexão com banco de dados."""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as e:
        logger.error(f"Erro de banco de dados: {e}")
        raise
    finally:
        conn.close()

def adicionar_favorito(user_id: str, team_id: int) -> bool:
    """Adiciona time aos favoritos."""
    try:
        with get_connection() as conn:
            conn.execute('''
                INSERT INTO favoritos (user_id, team_id) 
                VALUES (?, ?)
            ''', (user_id, team_id))
            conn.commit()
            logger.info(f"Favorito adicionado: {user_id} -> {team_id}")
            return True
    except sqlite3.IntegrityError:
        logger.debug(f"Favorito já existe: {user_id} -> {team_id}")
        return False
    except Exception as e:
        logger.error(f"Erro ao adicionar favorito: {e}")
        return False

def remover_favorito(user_id: str, team_id: int) -> bool:
    """Remove time dos favoritos."""
    try:
        with get_connection() as conn:
            cursor = conn.execute('''
                DELETE FROM favoritos 
                WHERE user_id = ? AND team_id = ?
            ''', (user_id, team_id))
            conn.commit()
            return cursor.rowcount > 0
    except Exception as e:
        logger.error(f"Erro ao remover favorito: {e}")
        return False

def obter_favoritos(user_id: str) -> list:
    """Retorna lista de IDs de times favoritos do usuário."""
    try:
        with get_connection() as conn:
            cursor = conn.execute('''
                SELECT team_id FROM favoritos 
                WHERE user_id = ? 
                ORDER BY data_criacao DESC
            ''', (user_id,))
            return [row['team_id'] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao obter favoritos: {e}")
        return []

def adicionar_pesquisa(user_id: str, termo: str):
    """Registra uma pesquisa no histórico."""
    try:
        if not termo or len(termo) < 2:
            return
        
        with get_connection() as conn:
            conn.execute('''
                INSERT INTO historico_pesquisas (user_id, termo) 
                VALUES (?, ?)
            ''', (user_id, termo))
            conn.commit()
    except Exception as e:
        logger.error(f"Erro ao registrar pesquisa: {e}")

def obter_historico_pesquisas(user_id: str, limite: int = 5) -> list:
    """Retorna últimas N pesquisas do usuário."""
    try:
        with get_connection() as conn:
            cursor = conn.execute('''
                SELECT DISTINCT termo FROM historico_pesquisas 
                WHERE user_id = ? 
                ORDER BY data DESC 
                LIMIT ?
            ''', (user_id, limite))
            return [row['termo'] for row in cursor.fetchall()]
    except Exception as e:
        logger.error(f"Erro ao obter histórico: {e}")
        return []

# Inicializar DB quando módulo é importado
try:
    init_db()
except Exception as e:
    logger.warning(f"⚠️ Não foi possível inicializar banco de dados: {e}")
