# pull official base image
FROM python:3.11

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Add database environment variables
ENV DB_NAME=postgres
ENV DB_USER=postgres
ENV DB_PASSWORD=123
ENV DB_HOST=localhost
ENV DB_PORT=5432

# OpenAI environment variables
ENV OPENAI_3_5_GENERATION_MODEL_NAME=""
ENV OPENAI_4_GENERATION_MODEL_NAME=""
ENV OPENAI_API_KEY=""

# install system dependencies
RUN apt-get update \
    && apt-get -y install netcat-openbsd gcc \
    && apt-get clean

# install python dependencies
RUN pip install --upgrade pip

# Poetry setup
RUN pip install poetry
RUN poetry config virtualenvs.create false

# copy project
COPY . /usr/src/app/

# Install dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# add app
COPY . ./

# expose port
EXPOSE 8080

# run
CMD poetry run uvicorn src.app:app --host=0.0.0.0 --port=8080
