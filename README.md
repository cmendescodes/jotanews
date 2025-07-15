
# 📡 JotaNews - Desafio Técnico Backend Python (JOTA)

Este projeto implementa uma solução robusta e escalável para ingestão, classificação, armazenamento e consulta de notícias. A arquitetura é baseada em microsserviços com uso de AWS SQS, Lambda com Docker e persistência em banco PostgreSQL via Railway.

---

## 🚀 Visão Geral

O objetivo é processar notícias enviadas via webhook, classificá-las automaticamente por categoria, subcategoria, urgência e tags, e armazená-las em banco de dados com uma API RESTful para consulta.

---

## 🔹 Funcionalidades Principais

- 📥 Recebimento de Webhooks via `POST /api/webhook/noticias/`
- 📨 Processamento assíncrono com fila de mensagens **Amazon SQS**
- 🏷️ Classificação baseada em palavras-chave
- 🐳 Execução da função Lambda com **Docker**
- 🛢️ Armazenamento em **PostgreSQL** (Railway)
- 📡 API REST para listagem e filtros por categoria, urgência e tags

---

## 🧑‍💻 Tecnologias Utilizadas

- **Linguagem & Frameworks**
  - Python 3.11
  - Django 4.x
  - Django REST Framework

- **Banco de Dados**
  - PostgreSQL (Railway)
  - Django ORM

- **Mensageria & Serverless**
  - Amazon SQS
  - AWS Lambda (Docker)
  - Amazon ECR

- **Containers & Deploy**
  - Docker (Multi-imagem: API e Lambda)
  - Gunicorn
  - Railway (com `railway.toml` opcional)

- **Ambiente & Configuração**
  - dotenv (.env)
  - CORS Headers (liberação para dev)

- **Testes**
  - Postman - via `/api/webhook/noticias`
  - `test_boto.py` -> Integração -> Dispara Notícias
  - `test_api.py` -> Unitário/Lambda-queue
  - (Planejado) pytest

- **DevOps e Ferramentas**
  - Git & GitHub
  - AWS CLI
  - Docker Hub / Amazon ECR
---

## 📊 Diagrama da Arquitetura


Cliente / Webhook
       -> POST /api
   Django REST API
       ->
 Railway + Gunicorn
       ->
 Recebe & envia para SQS
       ->
 Amazon SQS (noticias-queue)
       ->
     Trigger
       ->
 AWS Lambda (Docker + Django)
       ->
Classifica & salva no banco
       ->
PostgreSQL (Railway Cloud DB)


---

## 💡 Exemplo JSON para Webhook

```json
{
  "titulo": "Projeto de isenção do IR deve ser apresentado ao Congresso",
  "conteudo": "O projeto prevê mudanças no Imposto de Renda...",
  "fonte": "Jota",
  "data_publicacao": "2025-07-11T12:00:00Z",
  "urgente": false
}
```

---

## 🔄 Como Executar Localmente

1. **Clone o repositório:**

```bash
git clone https://github.com/cmendescodes/jotanews.git
```

2. **Configure o arquivo `.env`:**

```env
DJANGO_SECRET_KEY=your_secret_key
POSTGRES_DB=railway
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DB_HOST=your_host
POSTGRES_PORT=your_port
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=sa-east-1
SQS_QUEUE_URL=https://sqs.sa-east-1.amazonaws.com/.../noticias-queue
```

3. **Execute a aplicação:**

```bash
python manage.py migrate
python manage.py runserver
```

4. **Testar com Postman:**

```
http://127.0.0.1:8000/api/webhook/noticias/
```

---

## 🏐 Endpoints Principais

| Método | Rota                              | Descrição                           |
|--------|-----------------------------------|-------------------------------------|
| POST   | /api/webhook/noticias/           | Recebe notícias e envia para SQS    |
| GET    | /api/noticias/                   | Lista todas as notícias             |
| GET    | /api/noticias/?categoria=Poder   | Filtro por categoria                |
| GET    | /api/noticias/?tags=Reforma      | Filtro por tag                      |
| GET    | /api/noticias/?urgente=true      | Filtro por urgência                 |

---

## 🚫 Segurança

- Variáveis sensíveis isoladas no `.env`
- Servidor WSGI com Gunicorn para produção
- CORS liberado temporariamente com `CORS_ALLOW_ALL_ORIGINS=True` (desenvolvimento apenas)

---

## ⚖️ Testes

- Testes manuais via Postman
- Código `test_boto.py` com teste de integração -> envio de lote de notícias
- Código `test_api.py` com teste unitário -> sqs-queue
- Cobertura automatizada (sugestão: `pytest`)

---

## 🛠️ Deployment

- **API Django:** Deploy no Railway com Docker + Gunicorn
- **Lambda AWS:** Deploy com Docker e push para ECR
- **Railway:** Configurado via `railway.toml` caso tenha mais de um Dockerfile na raíz

---

## 📦 Instruções de Deployment

### Django API no Railway

- Dockerfile com Gunicorn:
```Dockerfile (raíz do projeto)
CMD sh -c "gunicorn jota_news.wsgi:application --bind 0.0.0.0:$PORT"
```
- Railway executa automaticamente - não precisa configurar Start Command.

### Lambda com Docker

- Dockerfile localizado no dir `lambda/Dockerfile`
- Antes do build da imagem Docker, mova o do dir `lambda/Dockerfile` Dockerfile para a raiz para facilitar:
```bash
docker build --provenance=false -t 123456789012.dkr.ecr.sa-east-1.amazonaws.com/jotanews:latest .

docker tag jotanews-lambda 123456789012.dkr.ecr.sa-east-1.amazonaws.com/jotanews:latest

docker push 123456789012.dkr.ecr.sa-east-1.amazonaws.com/jotanews:latest
```
- Atualize a função Lambda com essa imagem via ECR

---

### Deploy package Lambda via AWS CLI

- `package` localizado na raíz do projeto
```bash
zip -r package.zip .
aws configure -> (para logar no lambda)
aws lambda update-function-code --function-name nome-da-sua-funcao --zip-file fileb://lambda.zip --region us-east-1
```
---

### Variáveis Railway - Conferir REGIÃO DA FUNÇÃO Ex: sa-east-1

```env
DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,testserver
POSTGRES_DB=your_database_name
POSTGRES_USER=your_db_username
POSTGRES_PASSWORD=your_db_password
POSTGRES_PORT=sua porta
DB_HOST=your_database_host
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=sa-east-1
SQS_QUEUE_URL=https://sqs.sa-east-1.amazonaws.com/123456789012/your-queue-name
```

### Variáveis Lambda - Conferir REGIÃO DA FUNÇÃO Ex: sa-east-1

```env
DJANGO_SECRET_KEY=your_django_secret_key
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,testserver
POSTGRES_DB=your_database_name
POSTGRES_USER=your_db_username
POSTGRES_PASSWORD=your_db_password
POSTGRES_PORT=sua porta
DB_HOST=your_database_host
```
---

### ⚙️ Observação sobre CI/CD no GitHub Actions
❗ O workflow do GitHub Actions pode falhar inicialmente ao clonar o repositório, pois requer credenciais privadas do Docker Hub que não estão incluídas por questões de segurança.

Para ativar o CI/CD automático via GitHub Actions, após clonar o repositório para sua conta, insira as seguintes variáveis de ambiente no repositório do GitHub (Settings → Secrets → Actions):
```env
DOCKERHUB_USERNAME=seu-usuario-no-dockerhub
DOCKERHUB_TOKEN=seu-token-de-acesso
```
Essas variáveis são utilizadas para autenticar o push da imagem Docker da API/Lambda no workflow automático.
O projeto funcionará perfeitamente de forma manual ou local mesmo sem estas variáveis.

---

### ⚙️ Instruções staticfiles Painel Docker Admin

```bash
pip install whitenoise
```
Incluir manualmente ou
```bash
pip freeze > requirements.txt
```
**settings.py**
```bash
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # demais middlewares...
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

Após, acesse normalmente via https://seu-app.up.railway.app/admin

## 🎓 Autor

**Caio Mendes**  
🔗 [LinkedIn](https://www.linkedin.com/in/caiomanager-dev)  
📧 [mendesprogress@gmail.com](mailto:mendesprogress@gmail.com)

---

> ✨ *Pronto para integrar o envio de notificações via WhatsApp para notícias urgentes.*

---

&copy; 2025 CMendesDev para JotaNews. Todos os direitos reservados.
