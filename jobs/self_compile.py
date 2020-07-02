#!/usr/bin/env dronic
#
# self compile dronic
#

# load modules
git = plugin.load('git')    # git ops
docker = plugin.load('docker')

# globals
git_user = parameters.get('git_user','actee')
git_branch = parameters.get('git_branch','master')

docker_tag = parameters.get('docker_tag','self-compile')


@stage("Git checkout")
def checkout_code():

    if !workspace.exists('dronic'):
        git.clone(f'git@bitbucket.org:{git_user}/dronic.git')

    with workspace.dir('dronic'):
        git.fetch()
        git.checkout(git_branch)


@stage("Docker build")
def docker_build():

    with workspace.dir('dronic'):
        docker.build(file='deployment/Dockerfile',tag=docker_tag)
