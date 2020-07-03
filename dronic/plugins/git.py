#
# Git plugin for Dronic
#

import os
import re

re_repo_name = re.compile(r'[a-z0-9_-]+(?=(\.git)?$)')

from .. import Plugin

import dulwich.porcelain

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


    #
    # Git functions
    #

    def clone(repo):
        target_path = re_repo_name.findall(repo)[0]
        dulwich.porcelain.clone(repo, target=target_path)

    def checkout(branch, create=False):
        # see https://github.com/dulwich/dulwich/issues/576

        repo = dulwich.porcelain.Repo('.')

        branch_bytes = branch.encode()

        local_ref = b'refs/heads/%s' % branch_bytes
        remote_ref = b'refs/remotes/origin/%s' % branch_bytes

        if local_ref not in repo:
            # need to actually checkout

            # user should fetch first
            if remote_ref no in repo:
                # branch not available
                raise ValueError('unknown branch')

            # checkout from remote
            repo[local_ref] = repo[remote_ref]

            # update config file
            config = repo.get_config()
            config.set((b'branch',branch_bytes), b'remote', b'origin')
            config.set(b'branch',branch_bytes), b'merge', local_ref)
            config.write_to_path()

        # set head and build index
        old_head = repo[b'HEAD']
        old_tree = repo.get_object(old_head.tree)
        repo.refs.set_symbolic_ref(b'HEAD',local_ref)
        new_head = repo[b'HEAD']
        new_tree = repo.get_object(new_head.tree)
        repo.reset_index(head.tree)

        # TODO clean tree
        # remove files tracked in old_tree, but not tracked in new_tree
        old_files = set(self._list_files(repo,old_tree))
        new_files = set(self._list_files(repo,new_tree))
        # old_files - new_files -> files that are not in NEW but were in OLD
        to_remove = old_files-new_files
        for file in to_remove:
            os.remove(file)
        # and then, maybe, remove empty folders
        

    #
    # internal
    #

    def _list_files(self, repo, tree, parent=''):
        files = []
        for i in tree.iteritems():
            path = os.path.join(parent,i.path.decode())
            if i.mode == 16384:
                # folder
                files += self._list_files(
                    repo=repo,
                    tree=repo.get_object(i.sha),
                    parent=path
                )
                continue
            files.append(path)
        return files

plugin_class = GitPlugin
