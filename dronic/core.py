
from . import Credentials

class Core(object):
    
    def __init__(self,jobfile:str,argv:list,workspace:str):
        self._argv_ = argv
        self._jobfile_ = os.path.basename(jobfile)
        self._jobdir_ = os.path.dirname(os.getcwd()+'/'+jobfile)
        self._workspace_ = workspace

        # instead of having a separate credentials object
        # make it a property here
        self._credentials_ = Credentials()

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
    
    @property
    def credentials(self):
        return self._credentials_
