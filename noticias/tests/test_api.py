import os
import sys
import django
import json

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jota_news.settings')
django.setup()

from noticias.models import Noticia
from noticias.classification import classificar


class ClassificacaoTestCase(TestCase):
    def test_classificacao_simples(self):
        texto = "STF aprova novo teto de dedução no imposto de renda"
        categoria, subcategoria, tags = classificar(texto)
        self.assertIsNotNone(categoria)
        self.assertIsInstance(tags, list)


class WebhookAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse("webhook-noticias")  

    def test_envio_noticia_valida(self):
        payload = {
            "titulo": "Projeto de isenção do IR é apresentado",
            "conteudo": "Mudanças no imposto de renda são discutidas...",
            "fonte": "Jota",
            "data_publicacao": timezone.now().isoformat(),
            "urgente": False
        }

        response = self.client.post(
            self.url,
            data=json.dumps(payload),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Noticia.objects.filter(titulo__icontains="isenção").exists())

    def test_noticia_invalida(self):
        response = self.client.post(
            self.url,
            data=json.dumps({"titulo": "Faltando dados"}),
            content_type="application/json"
        )
        self.assertIn(response.status_code, [400, 422])

if __name__ == '__main__':
    import unittest
    unittest.main()