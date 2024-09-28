class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        self.description = 'UNKNOWN'
        self.version = '0.0.0'
        self.author = ''

    def initialize(self):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError

    def finalize(self):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError

class CredentialsPlugin(Plugin):

    def __init__(self):
        pass

class AgentPlugin(object):
    """Base class for Agent Provider plugin.
    """

    def __init__(self):
        pass

    def can_provide(self, *args, **kwds) -> bool:
        """Function called by Agent stage to ask if this plugin can provide
        an agent, based on the arguments passed by the developer.
        """
        raise NotImplementedError

    def provision(self, *args, **kwds) -> "multiprocessing.BaseManager":
        """Function called by agent to ask for a new `multiprocessing.Manager`,
        aka Agent.
        The plugin shall provision an agent and return an already connected
        `multiprocessing.BaseManager` (or a derivative class, TBD)
        """
        raise NotImplementedError

    def shutdown(self, manager: "multiprocessing.BaseManager"):
        """Function called by agent to signal that the agent is not longer
        needed.
        """
        raise NotImplementedError

