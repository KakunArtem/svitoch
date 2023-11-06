# svitoch

http://sum.in.ua/s/svitoch


## Project Overview

The project is organized into different modules and components.

- The `src` directory contains the source code of the application. We use `langchain` for core components and `FastAPI` for the REST API endpoint.
- The `src/rest_api` directory contains the REST API endpoints.


## Prerequisites
- Python 3.11.3
- poetry[https://python-poetry.org/docs/#installation]
- Docker[https://docs.docker.com/get-docker/]


## Contribution guidelines

### Setting up dev environment

1. Install dependencies:
```bash
poetry install --with dev
```

2. Set .env file with required properties:
- "OPENAI_API_KEY"
- "OPENAI_GENERATION_MODEL_NAME"

3. Start local server:
```bash
poetry run uvicorn src.rest_api.app:app --host=0.0.0.0 --port=8080 --reload
```
