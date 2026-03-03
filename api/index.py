import sys
import os

# Adicionar o diretório raiz ao path para importar app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Exportar a app Flask para Vercel como WSGI application
export = app

