import pytest
from rest_framework.test import APIClient
from noticias.models import Categoria, Subcategoria, Tag, Noticia
from django.utils import timezone

@pytest.mark.django_db
def setup_noticias():
    cat_trib = Categoria.objects.create(nome="Tributos")
    sub_apos = Subcategoria.objects.create(nome="Aposta da Semana", categoria=cat_trib)
    tag_ir = Tag.objects.create(nome="Imposto")

    Noticia.objects.create(
        titulo="Projeto IR",
        conteudo="Projeto de isenção do IR em debate",
        fonte="Jota",
        data_publicacao=timezone.now(),
        categoria=cat_trib,
        subcategoria=sub_apos,
        urgente=False
    ).tags.add(tag_ir)

    cat_saude = Categoria.objects.create(nome="Saúde")
    Noticia.objects.create(
        titulo="Campanha de vacinação",
        conteudo="Vacinação contra doenças",
        fonte="Agência",
        data_publicacao=timezone.now(),
        categoria=cat_saude,
        urgente=True
    )

@pytest.mark.django_db
def test_listar_noticias_com_filtros():
    setup_noticias()
    client = APIClient()

    # Testa filtro por categoria
    response = client.get('/api/noticias/', {'categoria__nome': 'Tributos'})
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]['categoria']['nome'] == 'Tributos'

    # Testa filtro por urgente
    response = client.get('/api/noticias/', {'urgente': True})
    assert response.status_code == 200
    assert all(n['urgente'] is True for n in response.json())

@pytest.mark.django_db
def test_busca_e_ordenacao():
    setup_noticias()
    client = APIClient()

    # Busca full text no título
    response = client.get('/api/noticias/', {'search': 'vacinação'})
    assert response.status_code == 200
    assert any('vacinação' in n['titulo'].lower() for n in response.json())

    # Ordena por data_publicacao descendente
    response = client.get('/api/noticias/', {'ordering': '-data_publicacao'})
    assert response.status_code == 200
