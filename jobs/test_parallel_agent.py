
@stage("Executed locally")
def locally():

	workspace.log("Executing locally")

# with Agent("x86_64"):
# 	@stage("on agent")
# 	def on_agent():
# 		workspace.log("Executing on agent")

with Parallel():
	@stage("parallel-1")
	def pll_1():
		workspace.log("Executing in parallel")

	@stage("parallel-2")
	def pll_2():
		workspace.log("Also in parallel")

