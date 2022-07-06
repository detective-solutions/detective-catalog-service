### BASE IMAGE
FROM python:3.10@sha256:850b7f7626e5ca9822cc9ac36ce1f712930d8c87eb31b5937dba4037fe204034 AS base

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
FROM python:3.10@sha256:850b7f7626e5ca9822cc9ac36ce1f712930d8c87eb31b5937dba4037fe204034

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
