(Docker build/run)

Build the Docker image from the repository root so the Docker build context contains `pyproject.toml` and `poetry.lock`:

```bash
# from repository root
docker build -f Dockerfile -t studioink-backend .

# run (exposes Django dev server on 8000)
docker run -p 8000:8000 studioink-backend
```

If you prefer building from `src/` keep the `src/Dockerfile` but use the root files as build context or modify its COPY lines to reference files inside `src/`.

## Docker Compose

Copy the example env and start the services:

```bash
cp .env.example .env
docker compose up --build
```

Bring the environment down with:

```bash
docker compose down -v
```

Notes:

- The `web` service mounts `./src` into the container so code changes are picked up without rebuilding.
- Database data is persisted in a Docker volume (`postgres_data`).
