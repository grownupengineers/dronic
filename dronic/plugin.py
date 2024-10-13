class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    # list of registered plugins, map from type to list
    REGISTERED = {}

    @classmethod
    def register(cls, plugin: type):
        allowed_types: set = {
            CredentialsPlugin,
            StepPlugin,
            AgentPlugin,
        }
        implemented_types = set(plugin.mro())
        intersection = set.intersection(allowed_types, implemented_types)

        if len(intersection) != 1:
            raise TypeError("Invalid plugin type")

        _type = intersection.pop()

        plugin_instance = plugin()

        try:
            cls.REGISTERED[_type].append(plugin_instance)
        except KeyError:
            cls.REGISTERED[_type] = [plugin_instance]

        return plugin_instance

    @classmethod
    def iter_plugins(cls, type_: type = None):
        if type_ is None:
            for list in cls.REGISTERED.values():
                yield from list
        else:
            try:
                yield from cls.REGISTERED[type_]
            except KeyError:
                yield from []

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

class StepPlugin(Plugin):
    """Base class for plugins that implement custom functions
    """

    # __init__, initialize, finalize do generally nothing
    def __init__(self): pass
    def initialize(self): pass
    def finalize(self): pass

    name: str = None

    def __call__(self, *args, **kwds):
        """Method called to invoke this plugin steps
        """
        raise NotImplementedError

class AgentPlugin(Plugin):
    """Base class for Agent Provider plugin.
    """

    def __init__(self):
        pass

    def can_provide(self, *args, **kwds) -> bool:
        """Function called by Agent stage to ask if this plugin can provide
        an agent, based on the arguments passed by the developer.
        """
        raise NotImplementedError

    def provision(self, *args, **kwds) -> "multiprocessing.managers.BaseManager":
        """Function called by agent to ask for a new `multiprocessing.Manager`,
        aka Agent.
        The plugin shall provision an agent and return an already connected
        `multiprocessing.BaseManager` (or a derivative class, TBD)
        """
        raise NotImplementedError

    def shutdown(self, manager: "multiprocessing.managers.BaseManager"):
        """Function called by agent to signal that the agent is not longer
        needed.
        """
        raise NotImplementedError

