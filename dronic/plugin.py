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
