from lssudoku import LSSudoku
from ilssudoku import ILSSudoku
from random import sample
from array import array
from copy import copy
from random import random
import cProfile

class GeneticSudoku(object):
	def __init__(self,N, Sud, prefill, poolSize=100):
		print "potato"
		self.prefill = prefill
		self.N = N

		self.population = set()
		self.heurvals = array('i', [20000]*poolSize)
		self.poolSize = poolSize
		
		tempsud = Sud(N,prefill = prefill)
		for i in range(poolSize):
			temptempsud =tempsud.copy()
			temptempsud.fill(prefill = prefill, possibleSwaps = tempsud.possibleSwaps)
			temptempsud.ity = i
			self.heurvals[i] = temptempsud.heuristicValue()
			
			self.population.add(temptempsud)

		#print self.crossOver(self.optima.pop(),self.optima.pop())

		self.solve()



	def solve(self, generations=1000, childAmount=0.1, acceptanceChance=0.5):
		
		for i in range(generations):
			parent = sample(self.population, 2 * int(self.poolSize * childAmount))
			parentTuples = set()
			while parent:
				parentTuples.add((parent.pop(), parent.pop()))
			children = set()
			newHeurs = copy(self.heurvals)
			while parentTuples:
				p1, p2 = parentTuples.pop()
				childHeur, child = self.crossOver(p1, p2)
				if childHeur == 0:
					return child
				newHeurs.append(childHeur)
				child.ity = len(newHeurs) - 1
				children.add(child)
			tournament = list(copy(self.population)) + list(children)
			def getHeurVal(sud):
				return newHeurs[sud.ity]
			tournament.sort(key=getHeurVal)
			finalPop = set()
			finalHeurs = []
			while len(finalPop) < self.poolSize:
				if random() > acceptanceChance:
					newIndividual = tournament[0]
					tournament = tournament[1:] # Select the individual and remove it from the tournament
				else:
					newIndividual = None
					chance = acceptanceChance * (1 - acceptanceChance)
					index = 1
					while newIndividual == None:
						if random() > chance:
							newIndividual = tournament[index]
							tournament = tournament[:index] + tournament[index+1:] # Select the individual and remove it from the tournament
						index += 1
						chance *= (1 - acceptanceChance)
						if index == len(tournament): # If none is accepted
							newIndividual = tournament[-1]
							tournament = tournament[:-1] # Accept the last one and remove it
				finalPop.add(newIndividual)
				finalHeurs.append(newHeurs[newIndividual.ity])
				newIndividual.ity = len(finalHeurs) - 1
			self.population = finalPop
			self.heurvals = array('i', finalHeurs)
		return self.population.pop()
			
			
			#print self.optima.pop().heuristicValue()

	def crossOver(self, sud1, sud2):
		""" """

		child = sud1.copy()

		for i in range(2* self.N**2, 3*self.N**2):
			units = sud1.unitlist[i]
			#block = random.sample([self.getValues(sud1, units), self.getValues(sud2, units)],1)
			if random() > 0.5:
				block = self.getValues(sud2, units)
				self.setValues(child,block,units)

		return child.hillClimb()

	def getValues(self,sud,squares):
		return [sud.getValue(sq=sq) for sq in squares]

	def setValues(self,sud,values,squares):
		for i in range(len(squares)):
			sud.setValue(values[i], sq=squares[i])

if __name__ == "__main__":
	def parse_3_grid(grid):
		"""Convert grid to a ILSSudoku(3), or return False if a contradiction
		is detected."""
		su = ILSSudoku(3)
		values = {}
		for i in range(len(grid)):
			if grid[i] not in "0.":
				y, x = divmod(i, 9)
				values[su.xy2sq(x, y)] = int(grid[i])
		su = GeneticSudoku(3, ILSSudoku, values)
		return su

	grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
	grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'

	#cProfile.run('sud.solve(restarts=10000, randomWalk=20)')
	sud = parse_3_grid(grid2)
	cProfile.run('a = sud.solve(generations=1000)')
	print(a)
	print(a.heuristicValue())
