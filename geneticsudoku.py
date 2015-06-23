from lssudoku import LSSudoku
from random import randrange
import copy, time, random

class GENETICSudoku(LSSudoku):
	def __init__(self, N, *args, **kwargs):
		super(ILSSudoku, self).__init__(N, *args, **kwargs)
		self.fill()

		self.values = self.generateSuccessor(self.values)

	def generateSuccessor(self, dictio):
if __name__ == "__main__":
	sud = GENETICSudoku(3)
	print(sud)
