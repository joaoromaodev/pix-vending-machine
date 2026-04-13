import os
import json
from pathlib import Path
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")
JSON_PATH = Path(__file__).parent.parent / "data" / "products.json"


def get_connection():
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Cria tabela de produtos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 0,
            image_url TEXT DEFAULT NULL
        )
    """)

    # Cria tabela de pagamentos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL DEFAULT 'pending',
            itens TEXT NOT NULL,
            total REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed: importa products.json se a tabela estiver vazia
    cursor.execute("SELECT COUNT(*) FROM produtos")
    result = cursor.fetchone()
    count = result['count']

    if count == 0 and JSON_PATH.exists():
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            produtos = json.load(f)
        for p in produtos:
            cursor.execute(
                "INSERT INTO produtos (id, name, price, stock) VALUES (%s, %s, %s, %s)",
                (p["id"], p["name"], p["price"], p["stock"])
            )
        print("✅ Seed: produtos importados do JSON para o PostgreSQL")

    conn.commit()
    cursor.close()
    conn.close()