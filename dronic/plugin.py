
from importlib import import_module

class Plugin(object):
    """Base class that each plugin must inherit from. within this class
    you must define the methods that all of your plugins must implement
    """

    def __init__(self):
        # name of the plugin, to be passed as global to job context
        self.name = "base_plugin"
        self.description = 'UNKNOWN'
        self.version = '0.0.0'
        self.author = ''

    def initialize(self):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError()

    def finalize(self):
        """The method that we expect all plugins to implement. This is the
        method that our framework will call
        """
        raise NotImplementedError()

class CredentialsPlugin(Plugin):

    def __init__(self):
        pass

_loaded = {}

# export this class as 'plugin'
class PluginFactory(object):

    # use 'global' _loaded, avoid security holes

    # load plugin by name
    # __please__, name the plugin file as the name of the plugin
    def load(name):
        if name in _loaded:
            return _loaded[name]
        try:
            mod = import_module(f'dronic.plugins.{name}')
        except ModuleNotFoundError:
            return None

        plugin = mod.plugin_class()
        plugin.initialize()

        _loaded[name] = plugin

        return plugin

    # finalize all plugins
    def finalize():
        for name in list(_loaded.keys()):
            _loaded[name].finalize()
            del _loaded[name]
        # okay
