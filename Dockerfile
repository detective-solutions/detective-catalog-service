### BASE IMAGE
FROM python:3.10-slim@sha256:df9e675c0f6f0f758f7d49ea1b4e12cf7b8688d78df7d9986085fa0f24933ade AS base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

WORKDIR /app

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python-dev

RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY . .

RUN pip install -r requirements.txt && \
    pip install -e . && \
    rm requirements.txt


### FINAL IMAGE
FROM python:3.10-slim@sha256:df9e675c0f6f0f758f7d49ea1b4e12cf7b8688d78df7d9986085fa0f24933ade

WORKDIR /app/venv

# Run application as non-root user
RUN groupadd -r detective && useradd -g detective --no-create-home detective && \
    chown -R detective:detective /app
USER detective

COPY --from=base /app/venv .
COPY . .

ENV PATH="/app/venv/bin:$PATH"
RUN chmod +x ./run-docker.sh

RUN ls -la

CMD ./run-docker.sh
