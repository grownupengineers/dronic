
from . import StageClass

#
# Dronic Pipeline
#
class Pipeline(object):

	def __init__(self):
		self._stages = []

	#
	# stage decorator
	#
	decorator = StageClass

	def run(self):
		success = True
		for stage in self._stages:
			print("Stage", stage.__name__)
			try:
				ret_val = stage()
				if not ret_val and ret_val is not None:
					raise Exception("Stage returned False")
			except Exception as e:
				print("Caught exception:", str(e))
				success = False
				break
		print("Pipeline status:", success)
		
