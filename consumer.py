import json
import django
import os
import sys
import time
from django.utils.dateparse import parse_datetime

# Setup Django
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings')
django.setup()

from noticias.models import Noticia, Categoria, Subcategoria, Tag
from noticias.classification import classificar

def save_noticia(data):
    """
    Recebe um dicionário com a notícia no formato:
    {
        "titulo": "Teste",
        "conteudo": "Conteúdo da notícia",
        "fonte": "Jota",
        "data_publicacao": "2025-07-10T14:00:00Z",
        "urgente": false
    }
    Classifica e salva no banco com categorias, subcategorias e tags.
    """
    try:
        titulo = data['titulo']
        conteudo = data['conteudo']
        fonte = data['fonte']
        data_publicacao_str = data['data_publicacao']
        urgente = data.get('urgente', False)

        data_publicacao = parse_datetime(data_publicacao_str)
        if data_publicacao is None:
            raise ValueError("data_publicacao inválida ou ausente")

        # Lógica de classificação por palavras-chave (sem IA)
        categoria_nome, subcategoria_nome, tags_nomes = classificar(f"{titulo} {conteudo}")

        # Buscar categoria existente (evita erro de duplicadas)
        categoria = Categoria.objects.filter(nome=categoria_nome or "Geral").first()
        if not categoria:
            categoria = Categoria.objects.create(nome=categoria_nome or "Geral")

        # Subcategoria com vínculo à categoria correta
        subcategoria = None
        if subcategoria_nome:
            subcategoria = Subcategoria.objects.filter(nome=subcategoria_nome, categoria=categoria).first()
            if not subcategoria:
                subcategoria = Subcategoria.objects.create(nome=subcategoria_nome, categoria=categoria)

        # Criar notícia
        noticia = Noticia.objects.create(
            titulo=titulo,
            conteudo=conteudo,
            fonte=fonte,
            data_publicacao=data_publicacao,
            categoria=categoria,
            subcategoria=subcategoria,
            urgente=urgente,
        )

        # Adicionar tags
        for tag_nome in tags_nomes:
            tag, _ = Tag.objects.get_or_create(nome=tag_nome)
            noticia.tags.add(tag)

        print(f"✅ Notícia salva: {titulo}")

    except Exception as e:
        print(f"❌ Erro ao salvar notícia: {e}")
        raise

# Callback RabbitMQ
def callback(ch, method, properties, body):
    print("📩 Mensagem recebida da fila")
    try:
        data = json.loads(body)
        save_noticia(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"❌ Erro no processamento da mensagem: {e}")
        # ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)  # Opcional

# Execução local com RabbitMQ
def main():
    import pika
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            print(f"✅ Conectado ao RabbitMQ: {rabbitmq_host}")
            break
        except Exception as e:
            print(f"❌ Tentativa {attempt+1} falhou: {e}")
            time.sleep(3)
    else:
        print("🚨 Erro: não foi possível conectar ao RabbitMQ.")
        return

    channel = connection.channel()
    channel.queue_declare(queue='noticias', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='noticias', on_message_callback=callback)
    print("🚀 Aguardando mensagens da fila...")
    channel.start_consuming()

# Execução via AWS Lambda (SQS)
def lambda_handler(event, context):
    try:
        records = event.get('Records', [])
        for record in records:
            data = json.loads(record['body'])
            save_noticia(data)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"{len(records)} notícias processadas com sucesso"})
        }

    except Exception as e:
        print(f"❌ Erro geral no processamento Lambda: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

# Execução local direta
if __name__ == '__main__':
    main()
