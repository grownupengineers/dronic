@stage("Executed locally")
def locally():

    workspace.log("Executing locally")


with Agent("podman", "dronic:latest"):
	@stage("on agent")
	def on_agent():
		workspace.log("Executing on agent")
		sh('pwd')
		sh('ls -l')

with Parallel():

    @stage("parallel-1")
    def pll_1():
        workspace.log("Executing in parallel")

    @stage("parallel-2")
    def pll_2():
        workspace.log("Also in parallel")

