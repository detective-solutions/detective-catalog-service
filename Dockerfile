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

# Add non-root user
RUN groupadd detective && \
    useradd -r -g detective --no-create-home detective
RUN mkdir /app && chown detective:detective /app

WORKDIR /app

COPY --chown=detective:detective --from=base /app/venv ./venv
COPY --chown=detective:detective . .
RUN chmod 750 ./run-docker.sh

# Run application as non-root user
USER detective

ENV PATH="/app/venv/bin:$PATH"
CMD ./run-docker.sh
