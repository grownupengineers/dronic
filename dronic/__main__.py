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

from .pipeline import Pipeline

# argv[1] -> pipeline file
# argv[2:] -> pipeline params

# We will provide a set of builtin API, this is just a POC
class DronicCore(object):

    def __init__(self,jobfile:str,argv:list,workspace:str):
        self._argv_ = argv
        self._jobfile_ = os.path.basename(jobfile)
        self._jobdir_ = os.path.dirname(os.getcwd()+'/'+jobfile)
        self._workspace_ = workspace

    def argv(self,idx):
        return self._argv_[idx]

    def log(self,*values):
        return print(*values)

    # Modules can only be loaded using this, we are in sandboxed environemnt
    def load_module(self,module):
        import importlib
        filepath = self._jobdir_+'/'+module.replace('.','/')+'.py'
        return importlib.machinery.SourceFileLoader(
            fullname=module, path=filepath).load_module()

    # We only allow access to files located on the pipeline source folder
    # or on the current workspace
    # TODO: this need to be improved is just a POC
    def open_file(self,path):
        
        filepath = self._jobdir_+'/'+path
        if os.path.exists(filepath):
            return open(file = self._jobdir_+'/'+path)
        print(filepath)
        filepath = self._workspace_+'/'+path
        if os.path.exists(filepath):
            return open(file = self._workspace_+'/'+path)
        print(filepath)

        return None

    # this have to return the workspace directory
    @property
    def workspace(self):
        return self._workspace_

    @property
    def jobfile(self):
        return self._jobfile_

    @property
    def jobdir(self):
        return self._jobdir_

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
    safe_globals['core'] = DronicCore(jobfile = argv[1],argv = argv[2:],workspace = workspace)

    job_locals = {}

    # The pipeline runs on a sandboxed environment with limited access
    byte_code = compile_restricted(contents, argv[0], 'exec')
    exec(byte_code, safe_globals,job_locals)

    pipeline.run()


except:
    print("Error opening or running pipeline")
    pass
