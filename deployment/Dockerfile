# build from dronic's top directory
# 'docker build --file deployment/Dockerfile --tag dronic:latest .'

# use slim image, < 200MB
FROM python:3-slim

ENV WORKSPACE /workspace
ENV JOBSPACE /jobs
# to include dronic
ENV PYTHONPATH /usr/src

# avoid installing everytime, run before dronic copy
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt && rm /tmp/requirements.txt


COPY deployment/entrypoint.sh /usr/local/bin/

RUN mkdir /workspace
WORKDIR /workspace
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# most likely to change
# dronic at /usr/src/dronic
COPY dronic /usr/src/dronic

# mount jobs as /jobs
