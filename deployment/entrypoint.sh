#!/bin/bash

# make sure we're there
test -d ${WORKSPACE} || { echo "mount jobs folder at /workspace"; exit 1; }
cd ${WORKSPACE}

export PYTHONPATH=/usr/src

# already using python(3) here
python -m dronic $@
