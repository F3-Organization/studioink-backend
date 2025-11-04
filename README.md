# StudioInk Backend

Backend da aplicação StudioInk, desenvolvido com Django REST Framework.

## Pré-requisitos

- **Python 3.13.7**: Gerenciado via [pyenv](https://github.com/pyenv/pyenv).
- **Poetry**: Para gerenciamento de dependências e tarefas [install](https://python-poetry.org/docs/#installation).
- **Docker e Docker Compose**: Para subir o ambiente completo (banco, Redis, RabbitMQ).
- **VS Code**: Recomendado para desenvolvimento, com o workspace configurado.

## Configuração Inicial

### 1. Clonagem e Ambiente Python

Clone o repositório:

```bash
git clone https://github.com/F3-Organization/studioink-backend.git
cd studioink-backend
```

Instale a versão do Python especificada:

```bash
pyenv install 3.13.7
pyenv local 3.13.7
```

### 2. Dependências com Poetry

Instale as dependências:

```bash
poetry install
```

Isso criará um ambiente virtual e instalará todas as dependências (produção e desenvolvimento).

### 3. Arquivo de Ambiente

Copie o arquivo de exemplo e configure as variáveis:

```bash
cp .env.example .env
```

Edite `.env` com suas configurações (ex.: chaves de API, senhas do banco).

## Subindo o Projeto

### Opção 1: Com Docker Compose (Recomendado para Desenvolvimento Completo)

Build e suba todos os serviços (API, banco PostgreSQL, Redis, RabbitMQ):

```bash
poetry run poe up
```

Ou diretamente:

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.

Para parar:

```bash
poetry run poe down
```

### Opção 2: Desenvolvimento Local (Sem Docker)

Se preferir rodar apenas a API localmente (banco e serviços externos via Docker):

Suba apenas os serviços externos:

```bash
docker compose up db redis rabbitmq
```

Ative o ambiente virtual e rode o servidor Django:

```bash
poetry shell
python manage.py migrate
python manage.py runserver
```

## Comandos Úteis

O projeto usa [Poe the Poet](https://github.com/nat-n/poethepoet) para tarefas personalizadas. Execute com `poetry run poe <comando>`.

### Docker

- `poetry run poe up`: Sobe todos os serviços.
- `poetry run poe down`: Para os serviços.
- `poetry run poe build`: Build das imagens.
- `poetry run poe logs`: Visualiza logs.
- `poetry run poe restart`: Reinicia serviços.
- `poetry run poe clean`: Limpa sistema Docker.

### Django

- `poetry run poe migrate`: Aplica migrações.
- `poetry run poe makemigrations`: Cria migrações.
- `poetry run poe shell`: Abre shell Django.
- `poetry run poe bash`: Abre bash no container da API.
- `poetry run poe createsuperuser`: Cria superusuário.

### Desenvolvimento

- `poetry run pytest`: Roda testes.
- `poetry run black .`: Formata código.
- `poetry run isort .`: Organiza imports.
- `poetry run ruff check .`: Linting.
- `poetry run mypy .`: Type checking.

## VS Code

Abra o workspace:

```bash
code studioink.code-workspace
```

O workspace já está configurado com:

- Formatação automática ao salvar (Black, isort, Ruff).
- Linting habilitado.
- Testes com pytest.
- Interpretador Python apontando para o venv do Poetry.

## Estrutura do Projeto

- `src/`: Código fonte da aplicação Django.
- `docker-compose.yaml`: Configuração dos serviços.
- `Dockerfile`: Imagem da API.
- `.env.example`: Exemplo de variáveis de ambiente.
- `pyproject.toml`: Configurações Poetry, dependências e tarefas.

## Contribuição

1. Instale pre-commit hooks: `poetry run pre-commit install`.
2. Siga conventional commits para mensagens.
3. Rode testes e linting antes de commitar.

## Licença

Proprietary
