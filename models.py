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
    import requests  # importa aqui para não quebrar nada

    if data is None:
        data = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO presencas (nome, telefone, motorista, cpf_motorista, qtde_pessoas, data)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, telefone, motorista, cpf_motorista, qtde_pessoas, data))
    conn.commit()

    # PEGAR O ID recém criado
    novo_id = cur.lastrowid

    conn.close()

    # ---------------------
    # CHAMA O N8N AUTOMÁTICO
    # ---------------------

    url_n8n = "https://n8n.vestelivre.com.br/webhook/rsvp_analuiza"

    payload = {
        "id": novo_id,
        "nome": nome,
        "telefone": telefone,
        "motorista": motorista,
        "cpf_motorista": cpf_motorista,
        "qtde_pessoas": qtde_pessoas,
        "data": data
    }

    try:
        requests.post(url_n8n, json=payload, timeout=5)
    except Exception as e:
        print("Falha ao chamar N8N:", e)




def listar_presencas():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            id,
            nome,
            telefone,
            motorista,
            cpf_motorista,
            qtde_pessoas,
            data
        FROM presencas
        ORDER BY id DESC
    """)
    rows = cur.fetchall()

    # transforma cada linha em dict pra ficar fácil de usar no template
    colunas = [desc[0] for desc in cur.description]
    presencas = [dict(zip(colunas, row)) for row in rows]

    conn.close()
    return presencas
