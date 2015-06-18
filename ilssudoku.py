from lssudoku import LSSudoku
from random import randrange
import copy, time, random

class ILSSudoku(LSSudoku):
	def __init__(self, N, *args, **kwargs):
		super(ILSSudoku, self).__init__(N, *args, **kwargs)
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

		svalue = 4

		for restarts in range(3):
			succ = dictio.copy()
			loopBest = 1000
			preClimbBest = 1000

			k = 0
			sameValues = 0
			randomWalked = False

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
					if sameValues == 3 and not randomWalked:
						preClimbBest = loopBest
						randomWalked = True
						sameValues = 0

						for i in range(svalue):
							succ = self.randomWalk(succ)
							loopBest = self.calcHeuristicFunc(succ)


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
		print bestHeur
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

	def randomWalk(self, dictio):
		randomSq = randrange(self.N**2)

		randomSpot = randrange(self.N**2)
		randomSpot2 = randrange(self.N**2)

		walkSquares = dictio.copy()

		square = self.unitlist[2*self.N**2 + randomSq]
		spot1 = square[randomSpot]
		spot2 = square[randomSpot2]

		walkSquares = self.swapSquare(walkSquares, spot1, spot2)

		# STATISTICS
		self.visitedStatesTotal += 1

		return walkSquares


	def swapSquare(self, dictio, sq1, sq2):
		""" Swaps the values of 2 squares in a given dictionary """
		val1 = dictio[sq1]
		val2 = dictio[sq2]

		dictio[sq1] = val2
		dictio[sq2] = val1
		return dictio


if __name__ == "__main__":
	sud = ILSSudoku(3)
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
