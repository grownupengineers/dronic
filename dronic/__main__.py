#!/usr/bin/env python3
#
# execute a pipeline (file)
#

import os
import argparse
from tempfile import mkdtemp
from RestrictedPython import compile_restricted
from RestrictedPython import safe_globals

from sys import argv

from . import Pipeline, Workspace, Builtins, Credentials

parser = argparse.ArgumentParser(prog="dronic",description="Runs a dronic pipeline script")
parser.add_argument("--workspace", default='.', help="set the workspace directory")
parser.add_argument("jobfile", default='main.py', help="set the name of the job to run")
parser.add_argument("params", nargs='*', help="the pipeline parameters")
args = parser.parse_args()

job_workspace = os.path.abspath(args.workspace)

if not os.path.exists(job_workspace):
    print("Workspace does not exists! Aborting....")
    exit(1)

try:
    job_params = {}
    for param in args.params:
        key, value = param.split('=',1)
        job_params[key] = value
except Exception as e:
    print("Error parsing parameters file:", str(e))
    exit(1)

if not os.path.exists(os.path.join(job_workspace,args.jobfile)):
    print("Job does not exists! Aborting....")
    exit(1)

try:
    fd = open(os.path.join(job_workspace,args.jobfile))
    contents = fd.read()
    fd.close()
except Exception as e:
    print("Error reading job file:", str(e))
    exit(1)

pipeline = Pipeline()

workspace = Workspace(workspace = job_workspace)
builtins = Builtins(job_params)
credentials = Credentials()

# new globals needed:
# - Parallel
# - Agent
safe_globals['stage'] = pipeline.decorator
safe_globals['parameters'] = builtins.parameters
safe_globals['_getitem_'] = builtins.safe_get_item
safe_globals['_write_'] = builtins.safe_write
# We will provide a set of API objects ( ie: credentials, git, docker, etc )
safe_globals['workspace'] = workspace
safe_globals['credentials'] = credentials

job_locals = {}

try:
    print("Compiling job...")
    # The pipeline runs on a sandboxed environment with limited access
    byte_code = compile_restricted(contents, argv[1], 'exec')
    exec(byte_code, safe_globals,job_locals)
except Exception as e:
    print("Error compiling job file:", str(e))
    exit(2)

try:
    print("Running job...")
    pipeline.run()
except Exception as e:
    print("Error running job file:", str(e))
    exit(3)

