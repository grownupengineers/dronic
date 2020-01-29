#!/usr/bin/env dronic
#
# --[execute with 'python3 -m dronic test_job.py]--
#
# execute with 'scripts/test_job.py'
# or 'dronic scripts/test_job.py'
#

@stage
def step1():
    module=core.load_module('module.mymodule')
    fd=core.open_file('resources/myresource.txt')
    if fd is not None:
        contents = fd.read()
        core.log(contents)
    fd.close()

    core.log(module.test_my_module())
    core.log(core.argv(0))
    core.log("this is step 1")

@stage
def creds():
    core.log("credentials example")

    secret_value = core.credentials('secret-value')
    fb_user,fb_pass = core.credentials('fb-creds')
