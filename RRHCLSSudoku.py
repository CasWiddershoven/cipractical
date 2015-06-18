from lssudoku import LSSudoku
from random import randrange
import copy, time, random

class RRHCLSSudoku(LSSudoku):
	def __init__(self, N, *args, **kwargs):
		super(RRHCLSSudoku, self).__init__(N, *args, **kwargs)
		self.fill()

		self.values = self.generateSuccessor(self.values)

	def generateSuccessor(self, dictio):
		""" Generates a random successor for the given state """

		# statistics
		self.visitedStatesTotal = 0
		self.visitedStates = {}

		# Variables used to determne the best successor
		bestHeur = self.calcHeuristicFunc(dictio)
		optimum = dictio.copy()
		succ = dictio.copy()

		sval = 4

		k = 0
		sameValues = 0

		for restarts in range(10):
			succ = dictio.copy()
			loopBest = 1000;

			k = 0
			sameValues = 0

			while sameValues < 3:
				print ""
				print k
				k +=1

				# pak een successor en de heuristical value ervan
				succ = self.hillClimb(succ).copy()
				heur = self.calcHeuristicFunc(succ)

				# vergelijk de value met de beste heuristical value
				if heur < loopBest:
					loopBest = heur
					sameValues = 0

					# als dit de beste tot nu toe gevondene is
					if heur < bestHeur:
						bestHeur = heur
						optimum = succ.copy()
						sameValues = 0

				if heur == loopBest:
					sameValues += 1

			# STATISTICS
			self.visitedStates[restarts] = self.visitedStatesTotal
			self.visitedStatesTotal = 0

		# STATISTICS
		# output the amount of states visited
		print self.visitedStates
		p=0
		for q in self.visitedStates:
			p += self.visitedStates[q]
		print p
		print ""

		return optimum

	def hillClimb(self, dictio):
		""" """
		bestSucc = dictio.copy()
		bestHeur = self.calcHeuristicFunc(dictio)

		unvisitedSquares = [0] * (self.N**2)
		sqPos = 1

		# Random selectie
		for sqPos in range(self.N**2):
			unvisitedSquares[sqPos] = copy.deepcopy(self.unitlist[2* self.N**2 + sqPos])

		startSquares = copy.deepcopy(unvisitedSquares)

		while sqPos and len(unvisitedSquares) > 1:
			sqPos = randrange(len(unvisitedSquares))

			# random selectie
			square1 = 1
			square2 = 1

			# nu beter:
			# Choose a random state to start swapping

			while square1 and len(startSquares[sqPos]) > 0:


				position1 = randrange(len(startSquares[sqPos]))
				square1 = startSquares[sqPos][position1]

				unvisitedSquares2 = copy.deepcopy(unvisitedSquares[sqPos])

				# we gotta preserve the original values
				if square1 in self.prefill:
					continue

				del unvisitedSquares2[position1]
				del unvisitedSquares[sqPos][position1]
				# remove the start every loop as well
				del startSquares[sqPos][position1]

				# Choose ALL other random states to swap with
				while square2 and len(unvisitedSquares2) > 0:
					currentSucc = dictio.copy()

					# STATISTICS
					self.visitedStatesTotal += 1

					# Pick another random square
					position2 = randrange(len(unvisitedSquares2))
					square2 = unvisitedSquares2[position2]

					# we gotta preserve the original values
					if square2 in self.prefill:
						del unvisitedSquares2[position2]
						continue

					if square1 == square2:
						del unvisitedSquares2[position2]
						continue


					# swap the values
					currentSucc = self.swapSquare(currentSucc, square1, square2)

					# Calculating the heuristical value
					currentHeur = self.calcHeuristicFunc(currentSucc)

					# we are done with the square, let's dispose it
					del unvisitedSquares2[position2]

					# Just in case
					if currentHeur == 0:
						return currentSucc

					# keeping the best successor
					if currentHeur < bestHeur:
						bestHeur = currentHeur
						bestSucc = currentSucc.copy()

				# einde van de start states

			# einde vierkant
			# When all possibles swaps in current big square have been considered
			# remove it
			del unvisitedSquares[sqPos]

		# DEBUG
		print bestHeur
		return bestSucc

	def swapSquare(self, dictio, sq1, sq2):
		""" Swaps the values of 2 squares in a given dictionary """
		val1 = dictio[sq1]
		val2 = dictio[sq2]

		dictio[sq1] = val2
		dictio[sq2] = val1
		return dictio



	def generateSucc(self):
		""" Generates and selects the most suited successor state for the sudoku """
		temp = self.calcHeuristicTmp()

		self.visitedStatesTotal = 0
		self.visitedStates = {}

		self.optimum = None

		# random restart hillclimbing
		for restarts in range(1):
			self.visitedStatesTotal = 0
			self.heur = temp

			self.successor = self.values.copy()
			self.optimum = self.values.copy()
			sameValues = 0
			value = 1000
			k = 0

			while sameValues < 3:
				print k
				k +=1
				self.successor = self.generateSuccHillClimb()

				if self.heur < value:
					self.optimum = self.successor.copy()

				if self.heur == value:
					sameValues +=1
				else:
					sameValues = 0
					value = self.heur


			self.visitedStates[restarts] = self.visitedStatesTotal

		self.values = self.optimum.copy()

		# output the amount of states visited
		print self.visitedStates
		p=0
		for q in self.visitedStates:
			p += self.visitedStates[q]
		print p
		print self.heur
		print ""

	def generateSuccHillClimb(self):
		""" Generates and checks all possible successor states and returns the best.
		The order in which it will check is completely random
		"""
		bestSuccessor = self.successor.copy()

		# Bekijk de heurstic values en sla de beste op
		bestHeur = self.heur #copy.deepcopy(self.heur)

		print bestHeur
		if bestHeur == 0:
			return bestSuccessor

		# nieuwe methode

		# en nu met random:
		unvisitedSquares = [0] * (self.N**2)
		sqPos = 1

		for sqPos in range(self.N**2):
			unvisitedSquares[sqPos] = copy.deepcopy(self.unitlist[2* self.N**2 + sqPos])

		while sqPos:
			sqPos = randrange(len(unvisitedSquares))

		#for sqPos in range(2*self.N**2,len(self.unitlist)):

			# elke square (0-8) gaat kijken of ie kan switchen ergens mee
			# for i in range(self.N**2):
			i = self.N**2
			# en nu random:
			while i:
				i-=1
				#sq1 = copy.deepcopy(self.unitlist[sqPos][i])
				sq1 = copy.deepcopy(unvisitedSquares[sqPos][i])

				# de originele posities moeten behouden blijven
				if sq1 in self.prefill:
					continue

				val1 = self.getValue(0,0,sq1)

				j = i
				while j < self.N**2 -1 :
					values = self.successor.copy()
					j += 1

					sq2 = unvisitedSquares[sqPos][j]

					# de originele posities moeten behouden blijven
					if sq2 in self.prefill:
						continue

					# For each visited state
					self.visitedStatesTotal += 1

					val2 = self.getValue(0,0,sq2)

					if val1 == val2:
						continue
					else:
						values[sq1] = val2
						values[sq2] = val1

						# Getting the heuristic
						currentHeur = self.calcHeuristicFunc(values)
						#print bestHeur
						#print currentHeur

						if currentHeur == 0:
							return values

						# Checking if it is the best heuristic value
						if  currentHeur < bestHeur:
							# Probeer deze eens zonder deepcopy!
							bestSuccessor = values.copy()#copy.deepcopy(values)
							bestHeur = copy.deepcopy(currentHeur)

			del unvisitedSquares[sqPos]
		# einde while loop

		if bestHeur < self.heur:
			self.heur = copy.deepcopy(bestHeur)

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
