import json
import pika
import django
import os
import sys
import time

# Configurar o ambiente Django para usar ORM fora do runserver
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings')
django.setup()

from noticias.models import Noticia, Categoria, Subcategoria, Tag
from noticias.classification import classificar

def save_noticia(data):
    """
    Salva notícia no banco de dados após classificar.
    Espera data com campos: titulo, conteudo, fonte, data_publicacao, urgente (bool)
    """
    titulo = data['titulo']
    conteudo = data['conteudo']
    fonte = data['fonte']
    data_publicacao = data['data_publicacao']
    urgente = data.get('urgente', False)

    # Classificar a notícia
    categoria_nome, subcategoria_nome, tags_nomes = classificar(titulo + " " + conteudo)

    categoria, _ = Categoria.objects.get_or_create(nome=categoria_nome or "Geral")
    subcategoria = None
    if subcategoria_nome:
        subcategoria, _ = Subcategoria.objects.get_or_create(nome=subcategoria_nome, categoria=categoria)

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

    # Criar ou obter tags e associar
    for tag_nome in tags_nomes:
        tag, _ = Tag.objects.get_or_create(nome=tag_nome)
        noticia.tags.add(tag)

    noticia.save()
    print(f"✅ Notícia salva: {titulo}")

def callback(ch, method, properties, body):
    print("📩 Mensagem recebida da fila")
    try:
        data = json.loads(body)
        save_noticia(data)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma que mensagem foi processada
    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")
        # Aqui você pode optar por não ack para tentar reprocessar, ou ack para descartar

def main():
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'rabbitmq')

    # Tentativa de conexão com retry
    max_retries = 10
    for attempt in range(max_retries):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
            print(f"✅ Conectado ao RabbitMQ no host '{rabbitmq_host}'")
            break
        except pika.exceptions.AMQPConnectionError as e:
            print(f"❌ Falha ao conectar ao RabbitMQ ({attempt+1}/{max_retries}): {e}")
            time.sleep(3)
    else:
        print("❌ Não foi possível conectar ao RabbitMQ após várias tentativas. Encerrando.")
        return

    channel = connection.channel()
    channel.queue_declare(queue='noticias', durable=True)

    channel.basic_qos(prefetch_count=1)  # Processa uma mensagem por vez
    channel.basic_consume(queue='noticias', on_message_callback=callback)

    print("🚀 Aguardando mensagens na fila 'noticias'. Para sair, pressione CTRL+C")
    channel.start_consuming()

if __name__ == '__main__':
    main()
