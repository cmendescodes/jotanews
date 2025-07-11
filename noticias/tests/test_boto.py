import boto3
import json
import uuid
from datetime import datetime

# Configure aqui o nome ou URL da sua fila SQS
SQS_QUEUE_URL = "https://sqs.sa-east-1.amazonaws.com/904368994684/noticias-queue"

sqs = boto3.client('sqs', region_name='sa-east-1')

def send_test_news_messages(n=20):
    for i in range(1, n+1):
        noticia = {
            "titulo": f"Notícia teste #{i}",
            "conteudo": "Conteúdo da notícia teste para demonstração do fluxo.",
            "fonte": "Script de Teste",
            "data_publicacao": datetime.utcnow().isoformat(),
            "urgente": i % 5 == 0  # marca uma a cada 5 como urgente
        }

        message_body = json.dumps(noticia)
        
        response = sqs.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=message_body
        )
        
        print(f"Mensagem {i} enviada, MessageId: {response.get('MessageId')}")

if __name__ == "__main__":
    send_test_news_messages()
