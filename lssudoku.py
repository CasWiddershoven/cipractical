from sudoku import Sudoku
import copy, time

class LSSudoku(Sudoku):
	def __init__(self, N, *args, **kwargs):
		super(LSSudoku, self).__init__(N, *args, **kwargs)
		self.fill()

		self.heur = self.calcHeuristic()

		for k in range(32):
			print k
			if k > 30:
				print self.values
			self.successor = self.generateSucc()
			self.values = self.successor

		print ""

	def fill(self):
		""" Fills the sudoku with a pre-chosen list and fills
		 in the rest with "random" numbers (1-9) """
		prefill = {513:4,514:2}
		for u in range(18,27):
		    for val in range(self.N**2):
		            self.setValue(val+1,0,0,self.unitlist[u][val])

		for u in prefill:
		    v = self.getValue(0,0,u)
		    s = self.units[u][2][prefill[u]-1]
		    self.setValue(prefill[u],0,0,u)
		    self.setValue(v,0,0,s)

	def calcHeuristic(self):
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
		_sum =0;

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
		""" Generates all possible successor states and returns the best """
		bestSuccessor = 0

		# Bekijk de heursitc values en sla de beste op
		bestHeur = self.heur

		print bestHeur
		if bestHeur==0:
			return self.values

		for i in range(len(self.squares)):
			sq = self.squares[i]

			# Deze moet gecopied worden
			restSq = copy.deepcopy(self.squares)
			del restSq[i]
			val1 = self.values[sq]

			for j in range(len(restSq)):
				sq2=restSq[j]

				values = copy.deepcopy(self.values)
				val2 = values[sq2]

				if val2 == val1:
					pass
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

		if bestHeur < self.heur:
			self.heur = bestHeur

		return bestSuccessor


if __name__ == "__main__":
	sud = LSSudoku(3)
	print(sud)
