import json
import os
import sys
import django

# Configura o ambiente Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings')
django.setup()

from noticias.models import Noticia, Categoria, Subcategoria, Tag
from noticias.classification import classificar


def save_noticia(data):
    titulo = data['titulo']
    conteudo = data['conteudo']
    fonte = data['fonte']
    data_publicacao = data['data_publicacao']
    urgente = data.get('urgente', False)

    categoria_nome, subcategoria_nome, tags_nomes = classificar(titulo + " " + conteudo)

    categoria, _ = Categoria.objects.get_or_create(nome=categoria_nome or "Geral")
    subcategoria = None
    if subcategoria_nome:
        subcategoria, _ = Subcategoria.objects.get_or_create(nome=subcategoria_nome, categoria=categoria)

    noticia = Noticia.objects.create(
        titulo=titulo,
        conteudo=conteudo,
        fonte=fonte,
        data_publicacao=data_publicacao,
        categoria=categoria,
        subcategoria=subcategoria,
        urgente=urgente,
    )

    for tag_nome in tags_nomes:
        tag, _ = Tag.objects.get_or_create(nome=tag_nome)
        noticia.tags.add(tag)

    noticia.save()
    print(f"✅ Notícia salva via Lambda: {titulo}")
    return noticia.id


def lambda_handler(event, context):
    """
    Handler da função Lambda.
    Espera `event` com os dados da notícia (JSON serializável).
    """
    try:
        if isinstance(event, str):
            event = json.loads(event)
        noticia_id = save_noticia(event)
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Notícia salva com sucesso!", "id": noticia_id})
        }
    except Exception as e:
        print(f"❌ Erro ao salvar notícia: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
