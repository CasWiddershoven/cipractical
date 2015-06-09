from lssudoku import LSSudoku
from random import randrange
import copy, time, random

class RRHCLSSudoku(LSSudoku):
	def __init__(self, N, *args, **kwargs):
		super(LSSudoku, self).__init__(N, *args, **kwargs)
		self.fill()

		self.generateSucc()

	def generateSucc(self):
		""" Generates and selects the most suited successor state for the sudoku """
		temp = self.calcHeuristicTmp()

		self.visitedStatesTotal = 0
		self.visitedStates = {}

		self.optimum = None

		# random restart hillclimbing
		for restarts in range(3):
			self.visitedStatesTotal = 0
			self.heur = temp

			self.successor = copy.deepcopy(self.values)
			self.optimum = copy.deepcopy(self.values)
			sameValues = 0
			value = 1000
			k = 0

			while sameValues < 3:
				print k
				k +=1
				self.successor = self.generateSuccHillClimb()
				if self.heur == value:
					sameValues +=1
				else:
					sameValues = 0
					value = self.heur
				if self.heur < value:
					self.optimum = self.successor

			self.visitedStates[restarts] = self.visitedStatesTotal

		self.values = self.optimum

		# output the amount of states visited
		print self.visitedStates
		p=0
		for q in self.visitedStates:
			p += self.visitedStates[q]
		print p
		print ""

	def generateSuccHillClimb(self):
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
	sud = RRHCLSSudoku(3)
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
