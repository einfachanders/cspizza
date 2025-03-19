FROM python:3.12-slim-bookworm AS builder

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y -q && apt-get upgrade -y -q \
    && apt-get install -y -q --no-install-recommends \
    gcc \
    git \
    python3-dev \
    &&  rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./requirements.txt /opt/pizza/requirements.txt
COPY ./app/ /opt/pizza/app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir \
    -r /opt/pizza/requirements.txt

FROM python:3.12-slim-bookworm AS runtime
LABEL maintainer="me@bitsheep.net"
LABEL description="pizza-backend"
LABEL version="v0.1.0"

USER root

# Preparations and upgrading operating system
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y -q && apt-get upgrade -y -q \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --gid="10000" --system pizza \
    && adduser --uid "10000" --ingroup "pizza" --home "/home/pizza" --shell "/bin/sh" --system --disabled-password --gecos "" pizza \
    && chown -R pizza:pizza \
    /home/pizza

# Install specific operating system packages
RUN apt-get update -y -q && apt-get upgrade -y -q \
    && apt-get install -y -q --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt /opt
RUN chown -R pizza:pizza /opt/pizza

# Make sure we use the virtualenv:
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
ENV SHELL=/bin/sh
ENV PYTHONUNBUFFERED=1

USER 10000

EXPOSE 8000/tcp
WORKDIR /opt/pizza
ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
