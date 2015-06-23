from lssudoku import LSSudoku
from ilssudoku import ILSSudoku
from random import sample
import random
import cProfile

class GeneticSudoku(object):
	def __init__(self,N, Sud, prefill, popSize=100):
		print "potato"
		self.prefill = prefill
		self.N = N


		self.optima = set()
		tempsud = Sud(N,prefill = prefill)
		for i in range(popSize):
			temptempsud =tempsud.copy()
			temptempsud.fill(prefill = prefill, possibleSwaps = tempsud.possibleSwaps)
			self.optima.add(temptempsud)
		
		print self.crossOver(self.optima.pop(),self.optima.pop())

	def crossOver(self, sud1, sud2):
		""" """

		child = sud1.copy()

		for i in range(2* self.N**2, 3*self.N**2):
			units = sud1.unitlist[i]
			#block = random.sample([self.getValues(sud1, units), self.getValues(sud2, units)],1)
			if random.random() > 0.5:
				block = self.getValues(sud2, units)
				self.setValues(child,block,units)

		return child

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
	parse_3_grid(grid1)
