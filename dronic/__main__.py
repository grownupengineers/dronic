#!/usr/bin/env python3
#
# execute a pipeline (file)
#

import os
from tempfile import mkdtemp
from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals
from RestrictedPython.PrintCollector import PrintCollector

from sys import argv

from . import Pipeline, Core

# argv[1] -> pipeline file
# argv[2:] -> pipeline params

try:
    # TODO: we must create
    fd = open(argv[1])
    contents = fd.read()
    fd.close()

    workspace = mkdtemp()

    pipeline = Pipeline()
    stage = pipeline.decorator

    safe_globals['stage'] = stage
    # We will provide a set of API objects ( ie: credentials, git, docker, etc ) 
    safe_globals['core'] = Core(jobfile = argv[1],argv = argv[2:],workspace = workspace)

    job_locals = {}

    # The pipeline runs on a sandboxed environment with limited access
    byte_code = compile_restricted(contents, argv[0], 'exec')
    exec(byte_code, safe_globals,job_locals)

    pipeline.run()


except:
    print("Error opening or running pipeline")
    pass
