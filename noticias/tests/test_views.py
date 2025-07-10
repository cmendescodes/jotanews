import pytest
from unittest import mock
from rest_framework.test import APIClient
from django.urls import reverse

@pytest.mark.django_db
@mock.patch("noticias.views.pika.BlockingConnection")
def test_webhook_api_recebe_noticia(mock_pika):
    # Mock da conexão e canal do RabbitMQ
    mock_channel = mock.Mock()
    mock_conn = mock.Mock()
    mock_conn.channel.return_value = mock_channel
    mock_pika.return_value = mock_conn

    client = APIClient()
    url = reverse('webhook-noticias')

    payload = {
        "titulo": "Isenção de IR será debatida no Congresso",
        "conteudo": "A proposta de isenção está sendo preparada.",
        "fonte": "Jota",
        "data_publicacao": "2025-07-10T14:00:00Z",
        "urgente": False
    }

    response = client.post(url, payload, format='json')
    assert response.status_code == 200
    assert "Notícia recebida" in response.data["detail"]

    # Verifica se publicamos algo na fila (mockado)
    mock_channel.queue_declare.assert_called_once()
    mock_channel.basic_publish.assert_called_once()
