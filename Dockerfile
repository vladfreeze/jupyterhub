ARG BUILDER_IMAGE=python:3.9-buster
ARG BASE_IMAGE=jupyterhub/k8s-hub:2.0.0
FROM $BUILDER_IMAGE AS builder
USER root

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get upgrade -yq\
   && apt-get install -yq --no-install-recommends \
      build-essential \
      ca-certificates \
      locales \
      python3-dev \
      python3-pip \
      python3-pycurl \
      nodejs \
      npm \
   && apt-get clean \
   && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade setuptools pip build wheel \
   && python3 -m pip install kubernetes

WORKDIR /tmp/jupyterhub
COPY . /tmp/jupyterhub/


WORKDIR /tmp/jupyterhub/jsx
# Build client component packages (they will be copied into ./share and
# packaged with the built wheel.)
RUN npm install --global yarn n
RUN n stable \
   && npm run build \
   && npm run place

WORKDIR /tmp/jupyterhub
# Build client component packages ( will be copied into ./share and
# packaged with the built wheel.)

RUN python3 -m build --wheel \
   && python3 -m pip wheel --wheel-dir /tmp/wheelhouse dist/*.whl


FROM $BASE_IMAGE as base

USER root

COPY --from=builder /tmp/wheelhouse /tmp/wheelhouse


RUN python3 -m pip uninstall jupyterhub --yes \
    && python3 -m pip install --no-cache /tmp/wheelhouse/* \
    && python3 -m pip install ldap3 \
    && python3 -m pip install kubernetes

RUN apt-get update && apt-get upgrade -yq \
   && apt-get purge -yq \
      vim \
      vim-runtime \
      vim-common \
      git \
      dnsutils \
      libexpat1 \
   && apt-get autoremove -yq && apt-get clean \
   && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /srv/jupyterhub/
WORKDIR /srv/jupyterhub
USER ${NB_USER}

