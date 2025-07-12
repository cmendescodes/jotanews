import boto3
import json
import random
from datetime import datetime, timedelta
import time

# Configuração da fila SQS
SQS_QUEUE_URL = "https://sqs.sa-east-1.amazonaws.com/904368994684/noticias-queue"
sqs = boto3.client('sqs', region_name='sa-east-1')

# Palavras-chave e categorias para simular as notícias
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

# Gera uma notícia simulada com palavras-chave relevantes
def gerar_noticia(i):
    categorias_keywords = [
        ("Governo anuncia nova isenção fiscal", "isencao fiscal"),
        ("Avanço da vacinação contra gripe", "vacina"),
        ("Sindicato discute reforma trabalhista", "sindicato"),
        ("Congresso aprova aumento no IR", "IR"),
        ("Hospitais enfrentam nova demanda de pacientes", "hospital"),
        ("Presidente sanciona novo decreto econômico", "decreto"),
        ("FGTS poderá ser usado para novas modalidades", "FGTS"),
        ("Expectativas para semana no Senado", "senado"),
        ("Resumo matinal: decisões do STF", "STF"),
        ("Vacina da dengue tem resultados positivos", "vacina")
    ]
    
    # Garantir que a categoria e o conteúdo possuem palavras-chave relevantes
    titulo, palavra_chave = random.choice(categorias_keywords)
    conteudo = random.choice(CONTEUDOS)
    conteudo += f" A palavra-chave associada é {palavra_chave}."  # Garantir que a palavra-chave esteja no conteúdo

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

# Envia as mensagens para a fila SQS
def send_test_news_messages(n=20, delay=0.2):
    for i in range(1, n+1):
        noticia = gerar_noticia(i)
        message_body = json.dumps(noticia)
        
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=message_body
        )
        
        print(f"📨 Notícia {i} enviada: {noticia['titulo']}")
        time.sleep(delay)  # Pausa entre envios para simular o fluxo real

    print(f"\n✅ {n} notícias enviadas com sucesso.")

if __name__ == "__main__":
    send_test_news_messages()
