from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebhookNoticiasView, NoticiaViewSet

router = DefaultRouter()
router.register(r'noticias', NoticiaViewSet, basename='noticia')

urlpatterns = [
    path('webhook/noticias/', WebhookNoticiasView.as_view(), name='webhook-noticias'),
    path('', include(router.urls)),
]
