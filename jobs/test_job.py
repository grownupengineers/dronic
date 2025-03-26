#!/usr/bin/env dronic-cli
#
# mainly for testing parameters
#
# needs parameters: a, b and c


@stage("Load resources and modules")
def step1():
    a = {"a": "b"}
    a["c"] = "d"
    workspace.log(a["a"])
    module = workspace.load_module("module.mymodule")
    fd = workspace.open("resources/myresource.txt")
    if fd is not None:
        contents = fd.read()
        workspace.log(contents)
    fd.close()

    workspace.log(module.test_my_module())
    workspace.log("this is step 1")


@stage("Load credentials")
def creds():
    workspace.log("credentials example")

    workspace.log(parameters["a"])
    workspace.log(parameters["c"])

    try:
        parameters["a"] = "b"
    except:
        workspace.log("caught exception")
    # secret_value = workspace.credentials('secret-value')
    # fb_user,fb_pass = workspace.credentials('fb-creds')


@stage("Test sh")
def test_sh():
    out = sh("echo hello", return_stdout=True)
    workspace.log(f"output '{out.strip()}'")
