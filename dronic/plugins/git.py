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
    
    def checkout(self, branch):
        # like above
        repo = porcelain.Repo('.')

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
