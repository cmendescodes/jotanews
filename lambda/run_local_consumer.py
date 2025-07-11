# run_local_consumer.py

import json
from lambda_function import lambda_handler

# Simula uma mensagem vinda do SQS
event = {
    "Records": [
        {
            "body": json.dumps({
                "titulo": "Congresso aprova isenção de IR para pequenas empresas",
                "corpo": "A medida foi aprovada por unanimidade nesta terça-feira...",
                "fonte": "Jota",
                "data_publicacao": "2025-07-11T10:30:00"
            })
        }
    ]
}

lambda_handler(event, None)
