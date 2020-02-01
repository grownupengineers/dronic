#!/usr/bin/env dronic
#
# --[execute with 'python3 -m dronic test_job.py]--
#
# execute with 'scripts/test_job.py'
# or 'dronic scripts/test_job.py'
#

@stage
def step1():
    a = { 'a': 'b'}
    a['c'] = 'd'
    workspace.log(a['a'])
    module=workspace.load_module('module.mymodule')
    fd=workspace.open('resources/myresource.txt')
    if fd is not None:
        contents = fd.read()
        workspace.log(contents)
    fd.close()

    workspace.log(module.test_my_module())
    workspace.log("this is step 1")

@stage
def creds():
    workspace.log("credentials example")

    workspace.log(parameters['a'])
    workspace.log(parameters['c'])

    parameters['a'] = 'b'
    # secret_value = workspace.credentials('secret-value')
    # fb_user,fb_pass = workspace.credentials('fb-creds')
