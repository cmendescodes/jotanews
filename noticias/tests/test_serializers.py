from noticias.serializers import WebhookNoticiaSerializer
from datetime import datetime

def test_serializer_valido():
    data = {
        "titulo": "Exemplo",
        "conteudo": "Corpo da notícia",
        "fonte": "Jota",
        "data_publicacao": "2025-07-10T14:00:00Z",
        "urgente": True
    }
    serializer = WebhookNoticiaSerializer(data=data)
    assert serializer.is_valid()

def test_serializer_invalido_sem_titulo():
    data = {
        "conteudo": "Corpo da notícia",
        "fonte": "Jota",
        "data_publicacao": "2025-07-10T14:00:00Z",
        "urgente": False
    }
    serializer = WebhookNoticiaSerializer(data=data)
    assert not serializer.is_valid()
    assert "titulo" in serializer.errors
