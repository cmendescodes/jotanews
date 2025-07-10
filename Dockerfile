# Dockerfile

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copia o projeto
COPY . /app

# Instala dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install psycopg2-binary

CMD ["gunicorn", "jota_news.wsgi:application", "--bind", "0.0.0.0:8000"]
