# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.183.0/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6, 3.8
ARG VARIANT="3.9"

#FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}
FROM python:3.9.2-alpine3.13 as base

# [Option] Install Node.js
# ARG INSTALL_NODE="true"
# ARG NODE_VERSION="lts/*"
# RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PYTHONASYNCIODEBUG=1

WORKDIR /app

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

ENV DEBIAN_FRONTEND=noninteractive

RUN python -m venv /venv

# [Optional] Uncomment this section to install additional OS packages.

RUN apk add --update git
RUN apk add --update bash

# install flake8 and tox
RUN pip install flake8
RUN pip install tox

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1