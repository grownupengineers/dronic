class Builtins(object):

    def __init__(self,params:dict = {}):
        self.__params__ = params
        pass

    @property
    def parameters(self):
        return self.__params__

    def safe_get_item(self,obj,idx):
        return obj[idx]

    def safe_write(self,obj):
        if obj is self.__params__:
            raise PermissionError('This operation is not allowed!')
        return obj

