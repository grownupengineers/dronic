#!/bin/bash

# make sure we're there
test -d ${JOBSPACE} || { echo "mount jobs folder at /jobs"; exit 1; }
#cd ${WORKSPACE}

export PYTHONPATH=/usr/src

# already using python(3) here
python -m dronic $@
