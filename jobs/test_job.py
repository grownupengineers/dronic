#
# execute with 'python3 -m dronic test_job.py
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
def step2():
    core.log("this is step 2")
