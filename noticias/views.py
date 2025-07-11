import json
import boto3
from botocore.exceptions import ClientError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from .models import Noticia
from .serializers import WebhookNoticiaSerializer, NoticiaSerializer
from .filters import NoticiaFilter


class WebhookNoticiasView(APIView):
    def post(self, request):
        serializer = WebhookNoticiaSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # Inicializa o client do SQS (região e fila devem estar configuradas)
                sqs = boto3.client('sqs', region_name='sa-east-1')  # Ajuste a região
                
                queue_url = 'https://sqs.sa-east-1.amazonaws.com/904368994684/noticias-queue'  # Substitua pela sua URL da fila
                
                mensagem = json.dumps(serializer.validated_data, default=str)

                response = sqs.send_message(
                    QueueUrl=queue_url,
                    MessageBody=mensagem
                )
                
            except ClientError as e:
                return Response(
                    {"detail": f"Erro ao enviar mensagem para SQS: {str(e)}"},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE
                )

            return Response({"detail": "Notícia recebida e enviada para fila SQS."}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoticiaViewSet(viewsets.ModelViewSet):
    queryset = Noticia.objects.all().order_by('-data_publicacao')
    serializer_class = NoticiaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = NoticiaFilter
    search_fields = ['titulo', 'conteudo']
    ordering_fields = ['data_publicacao']
    ordering = ['-data_publicacao']
