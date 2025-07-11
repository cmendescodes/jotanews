# Dockerfile.railway

# Usar imagem base do Python
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install gunicorn

COPY . .

ENV DJANGO_SETTINGS_MODULE=jota_news.settings

# Adicione STATIC_ROOT para coletar arquivos estáticos
RUN python manage.py collectstatic --noinput

CMD sh -c "gunicorn jota_news.wsgi:application --bind 0.0.0.0:$PORT"
