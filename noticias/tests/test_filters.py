import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from noticias.models import Categoria, Subcategoria, Tag, Noticia
from django.utils import timezone

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def setup_noticias(db):
    # Criar categorias, subcategorias, tags e notícias para teste
    cat1 = Categoria.objects.create(nome="Tributos")
    cat2 = Categoria.objects.create(nome="Saúde")

    sub1 = Subcategoria.objects.create(nome="Aposta da Semana", categoria=cat1)
    sub2 = Subcategoria.objects.create(nome="Matinal", categoria=cat2)

    tag_ir = Tag.objects.create(nome="Imposto de Renda")
    tag_saude = Tag.objects.create(nome="Saúde Pública")

    n1 = Noticia.objects.create(
        titulo="Projeto de isenção do IR",
        conteudo="Conteúdo sobre IR",
        fonte="Jota",
        data_publicacao=timezone.now(),
        categoria=cat1,
        subcategoria=sub1,
        urgente=True,
    )
    n1.tags.add(tag_ir)

    n2 = Noticia.objects.create(
        titulo="Vacinas contra gripe",
        conteudo="Conteúdo saúde",
        fonte="Jota",
        data_publicacao=timezone.now(),
        categoria=cat2,
        subcategoria=sub2,
        urgente=False,
    )
    n2.tags.add(tag_saude)

    return [n1, n2]

def test_filtrar_por_categoria(api_client, setup_noticias):
    url = reverse('noticia-list')  # rota automática do ViewSet
    response = api_client.get(url, {'categoria__nome': 'Tributos'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['titulo'] == "Projeto de isenção do IR"

def test_filtrar_por_subcategoria(api_client, setup_noticias):
    url = reverse('noticia-list')
    response = api_client.get(url, {'subcategoria__nome': 'Matinal'})
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['titulo'] == "Vacinas contra gripe"

def test_filtrar_por_urgente(api_client, setup_noticias):
    url = reverse('noticia-list')
    response = api_client.get(url, {'urgente': True})
    assert response.status_code == 200
    assert all(n['urgente'] for n in response.data)

def test_search_titulo(api_client, setup_noticias):
    url = reverse('noticia-list')
    response = api_client.get(url, {'search': 'isenção'})
    assert response.status_code == 200
    assert any('isenção' in n['titulo'].lower() for n in response.data)

def test_ordering_data_publicacao(api_client, setup_noticias):
    url = reverse('noticia-list')
    response = api_client.get(url, {'ordering': '-data_publicacao'})
    assert response.status_code == 200
    datas = [n['data_publicacao'] for n in response.data]
    assert datas == sorted(datas, reverse=True)
