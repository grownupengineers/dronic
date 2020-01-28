#!/usr/bin/env python3
#
# execute a pipeline (file)
#

import os

from sys import argv

from .pipeline import Pipeline

# argv[1] -> pipeline file
# argv[2:] -> pipeline params

#if __name__ == '__main__':	# which certainly will be
pipeline = Pipeline()
stage = pipeline.decorator

job_globals = {
	'stage': stage,
	'args': argv[2:]
	# plus other plugins
}

fd = open(argv[1])
contents = fd.read()
fd.close()

compiled = compile(contents,argv[0],'exec')

exec(compiled, job_globals)

pipeline.run()
