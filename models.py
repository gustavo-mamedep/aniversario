import sqlite3
from pathlib import Path
from datetime import datetime

# Caminho do arquivo do banco (ficará ao lado do main.py)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "presencas.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS presencas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            motorista TEXT,
            cpf_motorista TEXT,
            qtde_pessoas INTEGER NOT NULL,
            data TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()


def salvar_presenca(nome, telefone, motorista, cpf_motorista, qtde_pessoas, data=None):
    if data is None:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO presencas (nome, telefone, motorista, cpf_motorista, qtde_pessoas, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, telefone, motorista, cpf_motorista, qtde_pessoas, data))
    conn.commit()
    conn.close()
