import pika
import json
from datetime import datetime, timedelta
import random
import time

# Configurações do RabbitMQ (ajuste se necessário)
RABBITMQ_HOST = "localhost"  # ou IP público se RabbitMQ estiver na nuvem
QUEUE_NAME = "noticias"

# Palavras-chave e simulações para gerar as notícias
TITULOS = [
    "Governo anuncia nova isenção fiscal",
    "Avanço da vacinação contra gripe",
    "Sindicato discute reforma trabalhista",
    "Congresso aprova aumento no IR",
    "Hospitais enfrentam nova demanda de pacientes",
    "Presidente sanciona novo decreto econômico",
    "FGTS poderá ser usado para novas modalidades",
    "Expectativas para semana no Senado",
    "Resumo matinal: decisões do STF",
    "Vacina da dengue tem resultados positivos"
]

CONTEUDOS = [
    "A proposta segue agora para sanção presidencial após ampla maioria dos votos.",
    "Especialistas analisam impactos econômicos e sociais da nova medida.",
    "A medida foi classificada como uma aposta da semana pelos analistas políticos.",
    "Congresso debate isenções para pequenos empresários.",
    "SUS anuncia novo programa de atendimento domiciliar.",
    "Resumo matinal traz destaques da manhã desta terça-feira.",
    "O governo federal anunciou um novo decreto que altera a regulamentação atual.",
    "A reforma trabalhista divide opiniões entre especialistas.",
    "Novas variantes da gripe geram alerta entre autoridades de saúde.",
    "O mercado reage às projeções da semana em Brasília."
]

# Gera uma notícia com dados simulados
def gerar_noticia(i):
    titulo = random.choice(TITULOS)
    conteudo = random.choice(CONTEUDOS)
    fonte = "Agência Jota"
    urgente = random.choice([True, False])
    data_publicacao = (datetime.now() - timedelta(hours=i)).isoformat()

    return {
        "titulo": titulo,
        "conteudo": conteudo,
        "fonte": fonte,
        "urgente": urgente,
        "data_publicacao": data_publicacao
    }

# Envia as mensagens para a fila
def enviar_noticias(qtd=20, delay=0.2):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    for i in range(qtd):
        noticia = gerar_noticia(i)
        channel.basic_publish(
            exchange='',
            routing_key=QUEUE_NAME,
            body=json.dumps(noticia),
            properties=pika.BasicProperties(delivery_mode=2)
        )
        print(f"📨 Notícia {i+1} enviada: {noticia['titulo']}")
        time.sleep(delay)  # pequena pausa para simular fluxo real

    connection.close()
    print(f"\n✅ {qtd} notícias enviadas com sucesso.")

if __name__ == "__main__":
    enviar_noticias()
