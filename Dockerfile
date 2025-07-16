# Use a imagem oficial do Python como base
FROM python:3.10-slim-buster

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app

# Cria o diretório de trabalho
WORKDIR $APP_HOME

# Instala as dependências do sistema
RUN apt-get update     && apt-get install -y --no-install-recommends gcc     && rm -rf /var/lib/apt/lists/*

# Copia o pyproject.toml e poetry.lock para instalar as dependências
COPY pyproject.toml poetry.lock* $APP_HOME/

# Instala o Poetry
RUN pip install poetry

# Instala as dependências do projeto usando Poetry
RUN poetry install --no-root --no-dev

# Copia o restante do código da aplicação
COPY . $APP_HOME/

# Coleta arquivos estáticos (se houver)
RUN python manage.py collectstatic --noinput

# Expõe a porta que o Gunicorn vai usar
EXPOSE 8000

# Comando para iniciar o Gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
