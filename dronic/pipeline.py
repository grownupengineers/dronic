import traceback

from . import StageClass


#
# Dronic Pipeline
#
class Pipeline(object):

    def __init__(self):
        pass

    #
    # stage decorator
    #
    decorator = StageClass

    def run(self):
        success = True
        for stage in StageClass.stages:
            print("Stage '%s'" % stage.name)
            try:
                ret_val = stage.run()
                if not ret_val and ret_val is not None:
                    raise Exception("Stage returned False")
            except Exception as e:
                print("Caught exception:", str(e))
                print(traceback.format_exc())
                success = False
                break
        print("Pipeline status:", success)
