# lambda_function.py

import json
import os
from dotenv import load_dotenv
from classification import classificar
from db import salvar_noticia

load_dotenv()  # Carrega variáveis do .env para uso local

def lambda_handler(event, context):
    """
    Função Lambda principal acionada pelo SQS.
    """
    for record in event['Records']:
        try:
            message = json.loads(record['body'])

            titulo = message.get("titulo", "")
            corpo = message.get("corpo", "")
            fonte = message.get("fonte", "")
            data_publicacao = message.get("data_publicacao", "")

            texto = f"{titulo} {corpo}"
            categoria, subcategoria, tags = classificar(texto)

            noticia = {
                "titulo": titulo,
                "corpo": corpo,
                "fonte": fonte,
                "data_publicacao": data_publicacao,
                "categoria": categoria,
                "subcategoria": subcategoria,
                "tags": tags
            }

            salvar_noticia(noticia)

        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Processamento concluído com sucesso!')
    }
