#
# Git plugin for Dronic
#

import os

from .. import Plugin

from dulwich import porcelain

class GitPlugin(Plugin):

    def __init__(self):
        self.name = 'git'
        self.description = 'Git Plugin for Dronic'
        self.version = '0.0.0'
        self.author = "Tiago Teixeira <tiago.t@sapo.pt>"
    
    def initialize(self):
        pass
    
    def finalize(self):
        pass
    
    # clone a repository to target directory
    # eventually changing to branch
    #
    # git.clone('git@bitbucket.org:alexpires/dronic.git', 'src/dronic', 'feature/clone')
    def clone(self, remote, target, branch=None):
        # TODO sanitize target
        if not os.path.exists(target):
            # make it
            os.makedirs(target)
        
        if not os.path.isdir(target):
            raise Exception(f"{target} is not a directory")

        repo = porcelain.clone(remote, target)

        if branch is None:
            # just that
            return

        commit = repo.__getitem__(b'refs/remotes/origin/%s' % branch.encode())
        if commit is None:
            raise Exception(f"branch/commit {branch} not found")
        
        # fetch/pull branch from remote
        porcelain.pull(
            repo.path,
            remote,
            refspecs=[b'refs/heads/%s' % branch.encode()]
        )

        # checkout/build index
        repo.reset_index(commit.tree)
        # set head
        repo.refs.set_symbolic_ref(
            b"HEAD",
            b"refs/heads/%s" % branch.encode
        )
    
    def checkout(self, branch, location='.'):
        # like above
        repo = porcelain.Repo(location)

        commit = repo[b'refs/remotes/origin/%s' % branch.encode()]
        if commit is None:
            raise Exception(f"branch/commit {branch} not found")
        
        # get remote
        remote = repo.get_config()[(b'remote',b'origin')][b'url']

        # fetch/pull branch from remote
        porcelain.pull(
            repo.path,
            remote,
            refspecs=[b'refs/heads/%s' % branch.encode()]
        )

        # set head
        repo.refs.set_symbolic_ref(
            b"HEAD",
            b"refs/heads/%s" % branch.encode
        )
        # checkout/build index
        commit = repo[b'HEAD']
        repo.reset_index(commit.tree)
    
    def pull(self, location='.'):
        repo = porcelain.Repo(location)

        # get head refspec
        head = repo.refs.get_symrefs()[b'HEAD']

        # get remote
        remote = repo.get_config()[(b'remote',b'origin')][b'url']

        porcelain.pull(
            repo.path,
            remote,
            refspecs=[head]
        )

        # update index
        commit = repo[b'HEAD']
        repo.reset_index(commit.tree)

        # done
        

    # list branches
    @property
    def branches(self, location='.'):
        repo = porcelain.Repo(location)

        refs = [ref.decode() for ref in repo.get_refs().keys()]

        branches = []
        for ref in refs:
            if ref.startswith('refs/heads'):
                branch = ref.replace('refs/heads','',1))
            elif ref.startswith('refs/remotes/origin'):
                branch = ref.replace('refs/remotes/origin','',1))
            else:
                # wierd
                continue
            if branch not in branches:
                branches.append(branch)
        
        return branches

    @property
    def tags(self, location='.'):
        # TODO implement
        raise NotImplemented()
