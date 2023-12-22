# svitoch

- https://github.com/KakunArtem/svitoch
- http://sum.in.ua/s/svitoch

## Project Overview

The project is organized into different modules and components.

- The `src` directory contains the source code of the application. We use `langchain` for core components and `FastAPI`
  for the REST API endpoint.
- The `src/rest_api` directory contains the REST API endpoints.

## Prerequisites

- Python 3.11.3
- poetry[https://python-poetry.org/docs/#installation]
- postgres[https://www.postgresql.org/download/]
- Docker[https://docs.docker.com/get-docker/]

## Contribution guidelines

### Setting up dev environment

1. Install dependencies:

```bash
poetry install --with dev
```

2. Set .env file with required properties:

- "OPENAI_API_KEY"
- "OPENAI_3_5_GENERATION_MODEL_NAME"
- "OPENAI_4_GENERATION_MODEL_NAME"

3. Start Postgres SB. Do not forget to set the path where PostgreSQL data should be stored on your local machine using
   -v flag.

```bash
docker run --name svitoch_postgres -e POSTGRES_PASSWORD=123 -v SET_LOCAL_PATH -p 5432:5432 -d postgres
```

4. Start local server:

```bash
poetry run uvicorn src.rest_api.app:app --host=0.0.0.0 --port=8080 --reload
```

5. Swagger UI URL

```bash
http://localhost:8080/docs
```

6. Optional. UI app: https://github.com/KakunArtem/svitoch-ui

### Docker compose setup

### Environment Variables

This application requires the following environment variables to be set:

- `OPENAI_API_KEY`: Your OpenAI API key. Mandatory for interacting with the OpenAI API.
- `OPENAI_3_5_GENERATION_MODEL_NAME` and `OPENAI_4_GENERATION_MODEL_NAME`: Names of your OpenAI generation models.
- `POSTGRES_DATA_PATH`: The path where PostgreSQL data should be stored on your local machine.

Set these environment variables in your shell:

```bash
export OPENAI_API_KEY=your_openai_api_key
export OPENAI_3_5_GENERATION_MODEL_NAME=your_openai_3_5_generation_model_name
export OPENAI_4_GENERATION_MODEL_NAME=your_openai_4_generation_model_name
export POSTGRES_DATA_PATH=your_postgres_data_path
```

Or you can use an `.env` file to list the environment variables. Please reference the Docker Compose documentation for
how to accomplish this.

### Building Docker Image

To build the Docker image for the Python application, use the following command:

```bash
docker build -t your-image-name .
```

Replace `your-image-name` with the name you want to give to your Docker image.

### Docker Compose

To use Docker Compose to run the Python application and PostgreSQL database, use the following command:

```bash
docker-compose up
```

The Python application can access the PostgreSQL database on `localhost:5432`.

Please ensure you have set up all the required environment variables before running Docker-Compose command.