# aka podmanfile
ARG PYTHON_VER=3.12-slim
FROM python:${PYTHON_VER}

COPY . /dronic

RUN python3 -m pip install setuptools

RUN cd /dronic && python3 setup.py install

