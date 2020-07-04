#
# Git plugin for Dronic
#

import os
import re

re_repo_name = re.compile(r'([a-z0-9_-]+)(\.git)?$')

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

    def clone(self,repo, checkout=None):
        target_path = re_repo_name.search(repo).group(1)
        dulwich.porcelain.clone(repo, target=target_path)

        if checkout is not None and checkout isinstance(str):
            os.chdir(target_path)
            try:
                self.checkout(checkout)
            finally:
                os.chdir('..')
         # done clone

    def checkout(self,branch, create=False):
        # see https://github.com/dulwich/dulwich/issues/576

        repo = dulwich.porcelain.Repo('.')

        branch_bytes = branch.encode()

        local_ref = b'refs/heads/%s' % branch_bytes
        remote_ref = b'refs/remotes/origin/%s' % branch_bytes

        print(local_ref, remote_ref)

        if local_ref not in repo.refs:
            # need to actually checkout

            # user should fetch first
            if remote_ref not in repo.refs:
                # branch not available
                raise ValueError('unknown branch')

            # checkout from remote
            repo[local_ref] = repo[remote_ref]

        # update config file
        config = repo.get_config()
        section = (b'branch',branch_bytes)
        if section not in config:
            config.set(section, b'remote', b'origin')
            config.set(section, b'merge', local_ref)
            config.write_to_path()

        # set head and build index
        old_head = repo[b'HEAD']
        old_tree = repo.get_object(old_head.tree)
        new_head = repo[local_ref]
        new_tree = repo.get_object(new_head.tree)
        repo.refs.set_symbolic_ref(b'HEAD',local_ref)
        repo.reset_index(new_head.tree)
        index = repo.open_index()

        # TODO clean tree
        # remove files tracked in old_tree, but not tracked in new_tree
        old_files = set(self._list_files(repo,old_tree))
        new_files = set(self._list_files(repo,new_tree))
        # old_files - new_files -> files that are not in NEW but were in OLD
        to_remove = old_files-new_files
        dirs = set()    # to remove empty dirs
        for file in to_remove:
            dirs.add(os.path.dirname(file))
            os.remove(file)
            # also remove from index file
            del index[file.encode()]
        # and then, maybe, remove empty folders
        while len(dirs):
            for dir_ in reversed(list(dirs)):
                try:
                    len(os.listdir(dir_)) == 0 and os.rmdir(dir_)
                    dirs.remove(dir_)
                except OSError:
                    # probably not empty
                    pass
        #end while

        # save index
        index.write()

        # done checkout

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
