#
# Agent executor context manager
#

#
# inserts a wrapper stage that executed internal stages in a remote agent
#
# this is done by temporarily hijacking the StageClass's CONTAINER
#

from . import StageClass

class Agent(object):
	"""
		Stages defined inside an Agent context will get executed in a remote
		instance.

		By default, stages get executed locally.

		The arguments for the context manager will be passed to the Agent
		Provider plugins to determine where and how this will be executed

		The stages get executed sequentially.
	"""

	def __init__(self, *args, **kwds):
		self._args = args
		self._kwds = kwds
		self._stages = []
		self._save = None

	def __enter__(self):
		self._save = StageClass.CONTAINER
		StageClass.CONTAINER = self._stages

	def __exit__(self, _type, value, traceback):
		StageClass.CONTAINER = self._save
		parallel_stage = StageClass("Agent")(self._runner)

	def _runner(self):
		# TODO implement
		# figure out how to pass the stage code _and_ context to a remote
		# agent.
		#
		# _If_ both agent and "controller" are running the same python version,
		# the code object (bytecode) should be the same.
		#
		# `multiprocessing` has remote servers which may be a good starting
		# point for the implementation:
		# 1. spawn dronic with special `--agent` flag, possibly with labels;
		# 2. pass workspace/context (tar ball);
		# 3. agent reads pipeline file and finds stages for agent;
		# 3.1. agents exposes interfaces to execute those stages;
		# 4. when finished (signal), stop the agent.

		raise NotImplementedError

