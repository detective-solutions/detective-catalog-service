### BASE IMAGE
FROM python:3.10-slim@sha256:df9e675c0f6f0f758f7d49ea1b4e12cf7b8688d78df7d9986085fa0f24933ade

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python-dev

COPY . .

RUN pip install -r requirements.txt && \
    pip install -e . && \
    rm requirements.txt

# Run application as non-root user
RUN groupadd -r detective && useradd -g detective --no-create-home detective && \
    chown -R detective:detective .
USER detective

RUN ls -la

CMD uvicorn detective_catalog_service.service.server:app --host 0.0.0.0 --port 3003
