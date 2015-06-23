from sudoku import Sudoku
from random import randrange, randint
import copy, time, random

class LSSudoku(Sudoku):
	def __init__(self, N, *args, **kwargs):
		super(LSSudoku, self).__init__(N, *args, **kwargs)
		self.fill()
		
	def fill(self, file = None):
		""" Fills the sudoku with a pre-chosen list (can be read from file) and fills
		 in the rest with "random" numbers (1-9) """
		if file == None:
			self.prefill = {}
		else:
			f = open('sudoku.txt')
			self.prefill = f.read()
			f.close()
		for u in range(2* self.N**2,3* self.N**2):
		    for val in range(self.N**2):
		            self.setValue(val+1,0,0,self.unitlist[u][val])

		# in elke N^2 square in de sudoku
#		for u in range(2*self.N*2, 3*self.N**2):
#			posl = range(self.N**2)		# Posibilities list

#			val = randrange(len(posl))
#			index = 0
#			while val:
#				self.setValue(val+1,0,0,self.unitlist[u][index])
#				index+=1

				# DEBUG
#				print posl
#				print val

#				del posl[val]
#				val = randrange(len(posl))


		for u in self.prefill:
		    v = self.getValue(0,0,u)
		    s = self.units[u][2][self.prefill[u]-1]
		    self.setValue(self.prefill[u],0,0,u)
		    self.setValue(v,0,0,s)

	def calcHeuristicFunc(self, dictio):
		""" Calculates the heursitc value of an inputted sudoku """
		_sum = 0

		for u in self.unitlist:
		    for p in self.units[u[0]]:
		        nums = [0] *self.N**2
		        for i in p:
		            nums[dictio[i]-1] += 1
		        for j in nums:
		            if(j==0):
		                _sum += 1
		return _sum

	def generateSuccessor(self, dictio):
		""" Generates and checks all possible successor states and returns the best.
		The order in which it will check is completely random """
		return dictio

if __name__ == "__main__":
	sud = LSSudoku(3)
	print(sud)

	def switch(self, x1=None, x2=None, y1=None, y2=None, sq1=None, sq2=None):
		if sq1 == None:
			sq1 = self.xy2sq(x1, y1)
		if sq2 == None:
			sq2 = self.xy2sq(x2, y2)
		val1 = self.getValue(sq=sq1)
		val2 = self.getValue(sq=sq2)
		self.setValue(val2, sq=sq1)
		self.setValue(val1, sq=sq2)
