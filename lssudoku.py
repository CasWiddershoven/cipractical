from sudoku import Sudoku
from random import randrange
import copy, time, random

class LSSudoku(Sudoku):
	def __init__(self, N, *args, **kwargs):
		super(LSSudoku, self).__init__(N, *args, **kwargs)
		self.fill()

	def fill(self, file = None):
		""" Fills the sudoku with a pre-chosen list (can be read from file) and fills
		 in the rest with "random" numbers (1-9) """
		if file == None:
			self.prefill = {513:4,514:2, 520: 1}
		else:
			f = open('sudoku.txt')
			self.prefill = f.read()
			f.close()
		for u in range(18,27):
		    for val in range(self.N**2):
		            self.setValue(val+1,0,0,self.unitlist[u][val])

		for u in self.prefill:
		    v = self.getValue(0,0,u)
		    s = self.units[u][2][self.prefill[u]-1]
		    self.setValue(self.prefill[u],0,0,u)
		    self.setValue(v,0,0,s)

	def calcHeuristicTmp(self):
		""" Calculate the heurstic value for the initial sudoku """
		_sum =0;

		for u in self.unitlist:
		    for p in self.units[u[0]]:
		        nums = [0] * self.N**2
		        for i in p:
		            nums[self.values[i]-1] += 1
		        for j in nums:
		            if(j==0):
		                _sum += 1
		return _sum

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

	def generateSucc(self):
		""" Generates and checks all possible successor states and returns the best.
		The order in which it will check is completely random
		 """
		bestSuccessor = copy.deepcopy(self.successor)

		# Bekijk de heurstic values en sla de beste op
		bestHeur = copy.deepcopy(self.heur)

		print bestHeur
		if bestHeur == 0:
			return bestSuccessor
		usableSq = copy.deepcopy(self.squares)

		for i in range(len(self.squares)):
			sq = self.squares[i]

			# Deze moet gecopied worden
			restSq = copy.deepcopy(self.squares)

			# de originele posities moeten behouden blijven
			if sq in self.prefill:
				continue

			del restSq[i]

			val1 = self.successor[sq]

			# nu met random keuzes
			j = 1

			while j: #for j in range(len(restSq)):
				j = randrange(0,len(restSq))
				sq2 = restSq[j]

				# de originele posities moeten behouden blijven
				if sq2 in self.prefill:
					del restSq[j]
					continue

				values = copy.deepcopy(self.successor)
				val2 = values[sq2]

				if val2 == val1:
					del restSq[j]
					continue
				else:
					values[sq] = val2
					values[sq2] = val1
					currentHeur = self.calcHeuristicFunc(values)
					if currentHeur == 0:
						return copy.deepcopy(values)

					if  currentHeur < bestHeur:
						# Probeer deze eens zonder deepcopy!
						bestSuccessor = copy.deepcopy(values)
						bestHeur = currentHeur

				# random index keuze
				self.visitedStatesTotal += 1
				del restSq[j]


		if bestHeur < self.heur:
			self.heur = bestHeur

		return bestSuccessor


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
