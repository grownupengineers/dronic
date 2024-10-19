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
        self._save = StageClass.hijack(self._stages)

    def __exit__(self, _type, value, traceback):
        StageClass.restore(self._save)
        agent_stage = StageClass("Agent")(self._runner)

    def _runner(self):
        # TODO implement
        #
        # Iter all agent plugins and get first that "can provision" and
        # provision it.
        #
        # iter all stages and call the respective on the remote.

        raise NotImplementedError
