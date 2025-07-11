# db.py

import os
import psycopg2
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        port=os.environ.get("DB_PORT", 5432),
        dbname=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

def salvar_noticia(noticia: dict):
    """
    Insere uma notícia no banco PostgreSQL.
    Espera um dicionário com chaves: titulo, corpo, fonte, data_publicacao, categoria, subcategoria, tags
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO noticias (titulo, corpo, fonte, data_publicacao, categoria, subcategoria, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        noticia.get("titulo"),
        noticia.get("corpo"),
        noticia.get("fonte"),
        noticia.get("data_publicacao"),
        noticia.get("categoria"),
        noticia.get("subcategoria"),
        ','.join(noticia.get("tags", []))
    ))

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Notícia '{noticia.get('titulo')}' salva com sucesso.")

def listar_noticias(limit=10):
    """
    Retorna as últimas notícias cadastradas.
    """
    conn = get_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM noticias ORDER BY criada_em DESC LIMIT %s", (limit,))
    resultados = cur.fetchall()
    cur.close()
    conn.close()
    return resultados
