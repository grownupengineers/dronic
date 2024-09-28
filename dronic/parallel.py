#
# Parallel context manager
#

#
# inserts a wrapper stage that executes internals stages in parallel
#
# this is done by temporarily hijacking the StageClass's CONTAINER
#

from . import StageClass

class Pipeline(object):
	"""
		Stages defined inside a Pipeline context will get executed in parallel
	"""

	def __init__(self):
		self._stages = []
		self._save = None

	def __enter__(self):
		self._save = StageClass.CONTAINER
		StageClass.CONTAINER = self._stages

	def __exit__(self, _type, value, traceback):
		StageClass.CONTAINER = self._save
		parallel_stage = StageClass("Parallel")(self._runner)

	def _runner(self):
		# TODO implement
		# `multiprocessing` may be a good choice on how to do it
		raise NotImplementedError

