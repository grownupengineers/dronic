class Builtins(object):

    def __init__(self):
        pass

    def safe_get_item(self,obj,idx):
        return obj[idx]

    def safe_write(self,obj):
        return obj