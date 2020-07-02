import os

class Workspace(object):
    '''
    This class contains all available objects to interact with the building 
    workspace
    '''

    def __init__(self, workspace: str):
        self._workspace_ = os.path.abspath(workspace)

    def log(self, *values):
        return print(*values)

    # Modules can only be loaded using this, we are in sandboxed environemnt
    def load_module(self, module):

        import importlib

        module = module.replace('.', '/')+'.py'
        filepath = os.path.join(self._workspace_,module)
        
        if os.path.abspath(filepath).startswith(self._workspace_):
            return importlib.machinery.SourceFileLoader(fullname=module, path=filepath).load_module() # pylint: disable=no-value-for-parameter

        raise ModuleNotFoundError(f"Module {module} not found!")
    
    def open(self, path: str, mode: str = 'r'):

        filepath = os.path.join(self._workspace_, path)

        if os.path.exists(filepath):
            if os.path.abspath(filepath).startswith(self._workspace_):
                return open(file=filepath, mode=mode)

        raise FileExistsError(f"File {path} not found!")

    # this have to return the workspace directory
    @property
    def workspace(self):
        return self._workspace_
    
    def mkdir(self, directory):
        # TODO maybe sanitize the directory
        os.mkdir(directory)

    def exists(self, path):
        return os.path.exists(path)

    def isfile(self, path):
        return os.path.isfile(path)

    def isdir(self, path):
        return os.path.isdir(path)
    
    #
    # class dir
    #
    # allow to change directory
    # used within a context
    #
    # with workspace.dir('src/backend'):
    #   compile_project()
    #   publish_project()
    #
    # TODO to move this class out of this class
    # maybe create a subpackage for workspace related
    # functions ?
    #
    class dir(object):

        def __init__(self, directory):
            # FIXME sanitize directory
            if not os.path.isdir(directory):
                raise FileNotFoundError(f"directory '{directory}' does not exist")
            self._from = os.getcwd()
            self._target = directory
        
        # enter context
        def __enter__(self):
            os.chdir(self._target)
            #return None
        
        # exit context
        def __exit__(self):
            os.chdir(self._from)
