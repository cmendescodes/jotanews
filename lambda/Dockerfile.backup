# Imagem base oficial da AWS Lambda com Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Evita criação de .pyc e força logs no stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho padrão para AWS Lambda
WORKDIR /var/task

# Copia o requirements.txt primeiro (para cache)
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --upgrade pip \
 && pip install -r requirements.txt \
 && pip install psycopg2-binary

# Copia o restante do código do projeto para dentro da imagem
COPY . .

# Configuração do handler padrão da Lambda
CMD ["consumer.lambda_handler"]
