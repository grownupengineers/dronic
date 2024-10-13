
import collections
import subprocess

from dronic.plugin import StepPlugin

class Sh(StepPlugin):

	description = "Execute shell command"
	version = '0.0.1'
	author = 'dronic'

	name = 'sh'

	def __call__(self, cmd:str, return_stdout=False):
		sh_cmd = ['sh', '-c', cmd]
		proc = subprocess.run(
			sh_cmd,
			capture_output=return_stdout,
			text=True,
		)

		if return_stdout:
			return proc.stdout
		return proc.returncode

