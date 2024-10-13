#!/usr/bin/env python3
#
# execute a pipeline (file)
#

import os
import argparse
from tempfile import mkdtemp
from RestrictedPython import compile_restricted
from RestrictedPython import safe_builtins
from importlib.metadata import entry_points

from sys import argv

from . import (
    Pipeline,
    Workspace,
    Builtins,
    Credentials,
    Parallel,
    Plugin,
)
# avoid all imports
from . import plugin as plugin_module

def cli():

    parser = argparse.ArgumentParser(prog="dronic",description="Runs a dronic pipeline script")
    parser.add_argument("-A", "--agent", action="store_true", help="run in agent mode")
    parser.add_argument("-P", "--agent-password", default='n0t_v3ry_s4fe', help="set password for agent")
    parser.add_argument("-p", "--agent-port", type=int, default=50004, help="set port for agent bind")
    parser.add_argument("-w", "--workspace", default='.', help="set the workspace directory")
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
    except Exception as e:
        print("Error reading job file:", str(e))
        exit(1)
    finally:
        fd.close()

    pipeline = Pipeline()

    workspace = Workspace(workspace = job_workspace)
    builtins = Builtins(job_params)
    credentials = Credentials()

    # load & initialize plugins
    dronic_plugins = entry_points(group='dronic.plugin')
    for plugin_ep in dronic_plugins:
        plugin_class = plugin_ep.load()
        if type(plugin_class) is not type:
            # fail silently
            continue
        try:
            instance = Plugin.register(plugin_class)
        except TypeError as e:
            print("Warn:", str(e))
            # ignore
            continue

        print(f"Loaded plugin {plugin_ep.name} v{instance.version}")

        # TODO handle exception
        instance.initialize()

    # new globals needed:
    # - Parallel
    # - Agent
    safe_globals = dict(
        stage=pipeline.decorator,
        parameters=builtins.parameters,
        # We will provide a set of API objects ( ie: credentials, git, docker, etc )
        workspace=workspace,
        credentials=credentials,
        Parallel=Parallel,
        __builtins__=safe_builtins
    )
    safe_builtins['_getitem_'] = builtins.safe_get_item
    safe_builtins['_write_'] = builtins.safe_write

    job_locals = {}
    # add custom/plugin steps to globals
    for plugin in Plugin.iter_plugins(plugin_module.StepPlugin):
        # TODO figure out if it's possible to use RestrictedPython to get these
        # plugins out of the globals. Maybe there's a __getattribute__ for the
        # builtins?
        safe_globals[plugin.name] = plugin

    try:
        print("Compiling job...")
        # The pipeline runs on a sandboxed environment with limited access
        byte_code = compile_restricted(contents, args.jobfile, 'exec')
        exec(byte_code, safe_globals,job_locals)
    except Exception as e:
        print("Error compiling job file:", str(e))
        raise e
        exit(2)

    if args.agent:
        # run in agent mode
        raise NotImplementedError
    else:
        # executing mode
        try:
            print("Running job...")
            pipeline.run()
        except Exception as e:
            print("Error running job file:", str(e))
            exit(3)

