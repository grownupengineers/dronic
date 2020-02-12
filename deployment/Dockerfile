# build from dronic's top directory
# 'docker build --file deployment/Dockerfile --tag dronic:latest .'

# use slim image, < 200MB
FROM python:3-slim

ENV WORKSPACE /workspace
# to include dronic
ENV PYTHONPATH /usr/src

# dronic at /usr/src/dronic
COPY dronic /usr/src/
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt

COPY deployment/entrypoint.sh /usr/local/bin/

WORKDIR /
ENTRYPOINT /usr/local/bin/entrypoint.sh

# mount jobs as /workspace