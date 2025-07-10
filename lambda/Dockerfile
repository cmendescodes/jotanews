FROM public.ecr.aws/lambda/python:3.11

# Copiar apenas o necessário
COPY lambda_handler.py classification.py requirements.txt ./

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Apontar o handler
CMD ["lambda_handler.lambda_handler"]
