# DEPRECATED, unused -- remove

#
# parse a job file in the context of parameters
#

import os

from RestrictedPython import (
	compile_restricted,
	safe_builtins,
)

from . import (
	Pipeline,
	Workspace,
	Builtins,
	Credentials,
	Parallel,
)

def parse_job(args):
	job_workspace = os.path.abspath(args.workspace)

	if not os.path.exists(job_workspace):
		raise Exception("Workspace does not exist")

	try:
		job_params = {}
		for param in args.params:
			key, value = param.split('=', 1)
			job_params[key] = value
	except Exception:
		raise Exception("Error parsing parameters")

	job_file = os.path.join(job_workspace, args.jobfile)

	if not os.path.exists(job_file):
		raise Exception("Job file does not exist")

	try:
		with open(job_file) as fd:
			contents = fd.read()
	except Exception:
		raise Exception("Error reading job file")

	pipeline = Pipeline()

	workspace = Workspace(job_workspace)
	builtins = Builtins(job_params)
	credentials = Credentials()

	safe_globals = dict(
		stage=pipeline.decorator,
		parameters=builtins.parameters,
		workspace=workspace,
		credentials=credentials
		Parallel=Parallel,
		__builtins__=safe_builtins,
	)
	safe_builtins['_getitem_'] = builtins.safe_get_item
	safe_builtins['_write_'] = builtins.safe_write

	job_locals = {}

	try:
		print("Compiling job...")
		byte_code = compile_restricted(contents, args.jobfile, 'exec')
		exec(byte_code, safe_globals, job_locals)
	except Exception:
		raise Exception("Error compiling job file")

	# return None

