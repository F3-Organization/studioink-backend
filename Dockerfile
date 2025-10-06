FROM python:3.13.7-alpine3.22
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

RUN pip install --upgrade pip
RUN pip install pipx
RUN pipx install poetry

# Copy dependency metadata first to leverage Docker cache when dependencies don't change
COPY pyproject.toml poetry.lock /app/
# Ensure poetry is available in PATH when installed by pipx
ENV PATH="/root/.local/bin:${PATH}"
# Disable poetry virtualenv creation so dependencies are installed into the container Python
ENV POETRY_VIRTUALENVS_CREATE=false
RUN poetry install --no-interaction --no-ansi --no-root

# Copy application source
COPY src/ /app/

EXPOSE 8000

# Default command (override when running)
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
