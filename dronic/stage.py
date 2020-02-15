#
# Stage class decorator
#

#
# supposed to be something like
#   @stage("A stage")
#   def stage_a():
#       # do stuff
#

class StageClass(object):

    # holds the stages declared
    #
    # this can be overriden
    # so that the list
    CONTAINER = []
    stages = CONTAINER

    name = property(lambda self : self._name)

    def __init__(self, name, *args, **kwargs):
        self._name = name
        # some args, because, why not?
        self._args = args
        self._kwargs = kwargs
        self._function = None
    
    def __call__(self, function):
        self._function = function
        StageClass.CONTAINER.append(self)
        return function
    
    def run(self):
        if self._function is None:
            return None # or throw exception
        return self._function()
    
    def __str__(self):
        return f'Stage "{self._name}"'
    
    __repr__ = __str__

    # static method
    # def stages():
    #     return StageClass.CONTAINER