# build from dronic's top directory
# 'docker build --file deployment/Dockerfile --tag dronic:latest .'
FROM python:3

ENV WORKSPACE /workspace
# to include dronic
ENV PYTHONPATH /usr/src

# dronic at /usr/src/dronic
COPY dronic /usr/src/
COPY deployment/entrypoint.sh /usr/local/bin/

ENTRYPOINT /usr/local/bin/entrypoint.sh

# mount jobs as /workspace