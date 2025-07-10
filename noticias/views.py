import json
import pika
from pika.exceptions import AMQPConnectionError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import Noticia
from .serializers import WebhookNoticiaSerializer, NoticiaSerializer
from .filters import NoticiaFilter  # import do filtro personalizado


class WebhookNoticiasView(APIView):
    def post(self, request):
        serializer = WebhookNoticiaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
                channel = connection.channel()
                channel.queue_declare(queue='noticias', durable=True)

                mensagem = json.dumps(serializer.validated_data, default=str)

                channel.basic_publish(
                    exchange='',
                    routing_key='noticias',
                    body=mensagem,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                    )
                )
                connection.close()
            except AMQPConnectionError:
                return Response(
                    {"detail": "Erro ao conectar na fila RabbitMQ."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )
            return Response({"detail": "Notícia recebida e enfileirada."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all().order_by('-data_publicacao')
    serializer_class = NoticiaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoticiaFilter
    search_fields = ['titulo', 'conteudo']
    ordering_fields = ['data_publicacao']
    ordering = ['-data_publicacao']
