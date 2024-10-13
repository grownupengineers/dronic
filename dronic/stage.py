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
    # can be hijacked to create compound stages
    CONTAINER = []
    # all stages, can't be hijacked
    # used by agents to export individual stages
    ALL = []
    stages = CONTAINER

    name = property(lambda self : self._name)

    def __init__(self, name: str, *args, **kwargs):
        self._name = name
        # some args, because, why not?
        self._args: list = args
        self._kwargs: dict = kwargs
        self._function: callable = None
        self._stage_id: int = -1

    def __call__(self, function):
        self._function = function
        self._stage_id = len(StageClass.ALL)
        StageClass.CONTAINER.append(self)
        StageClass.ALL.append(self)
        return function

    def run(self):
        if self._function is None:
            return None # or throw exception
        return self._function()

    def __str__(self):
        return f'Stage "{self._name}"'

    __repr__ = __str__

    @classmethod
    def hijack(cls, container: list) -> list:
        save = cls.CONTAINER
        cls.CONTAINER = container
        return save

    @classmethod
    def restore(cls, save: list):
        cls.CONTAINER = save

    @classmethod
    def get_stage(stage_id: int):
        for stage in cls.ALL:
            if stage._stage_id == stage_id:
                return stage
        return None

    # static method
    # def stages():
    #     return StageClass.CONTAINER

