# python:3.10-slim
FROM python@sha256:df9e675c0f6f0f758f7d49ea1b4e12cf7b8688d78df7d9986085fa0f24933ade

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e . && \
    rm requirements.txt

# Run application as non-root user
RUN groupadd -r detective && useradd -g detective --no-create-home detective && \
    chown -R detective:detective /app
USER detective

CMD uvicorn detective_catalog_service.service.server:app --host 0.0.0.0 --port 3003
