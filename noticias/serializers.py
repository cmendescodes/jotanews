from rest_framework import serializers
from .models import Categoria, Subcategoria, Tag, Noticia

class WebhookNoticiaSerializer(serializers.Serializer):
    titulo = serializers.CharField(max_length=255)
    conteudo = serializers.CharField()
    fonte = serializers.CharField(max_length=255)
    data_publicacao = serializers.DateTimeField()
    urgente = serializers.BooleanField(default=False)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nome']

class SubcategoriaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Subcategoria
        fields = ['id', 'nome', 'categoria']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nome']

class NoticiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Noticia
        fields = '__all__'

class NoticiaSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    subcategoria = SubcategoriaSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Noticia
        fields = [
            'id',
            'titulo',
            'conteudo',
            'fonte',
            'data_publicacao',
            'categoria',
            'subcategoria',
            'tags',
            'urgente',
        ]
