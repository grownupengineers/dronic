# I'm not sure what is supposed to happen

@stage("the outer stage")
def outer():
    workspace.log("defining another stage inside")

    @stage("inner")
    def inner():
        workspace.log("yes")

@stage("another outer stage")
def outer2():
    workspace.log("dred")

