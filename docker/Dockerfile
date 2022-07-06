### BASE IMAGE
FROM python:3.10-slim@sha256:df9e675c0f6f0f758f7d49ea1b4e12cf7b8688d78df7d9986085fa0f24933ade as base

WORKDIR /usr/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python-dev

RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt
COPY . .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install -e . && \
    rm requirements.txt


### FINAL IMAGE
FROM python:3.10-slim@sha256:df9e675c0f6f0f758f7d49ea1b4e12cf7b8688d78df7d9986085fa0f24933ade

WORKDIR /usr/app/venv

# Run application as non-root user
RUN groupadd -r detective && useradd -g detective --no-create-home detective && \
    chown -R detective:detective /usr/app/venv
USER detective

COPY --from=base /usr/app/venv ./venv
COPY . .

ENV PATH="/usr/app/venv/bin:$PATH"

CMD uvicorn detective_catalog_service.service.server:app --host 0.0.0.0 --port 3003
