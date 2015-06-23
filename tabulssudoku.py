from lssudoku import LSSudoku
from random import sample
import cProfile

class TabuLSSudoku(LSSudoku):
	class TabuList:
		class TabuNode:
			def __init__(self, data, nxt):
				self.data = data
				self.nxt = nxt
		
		def __init__(self, length):
			self.length = length
			self.start = None
			
		def add(self, data):
			node = self.TabuNode(data, self.start)
			self.start = node
			
		def items(self):
			i = 0
			node = self.start
			while i < self.length and node != None:
				yield node.data
				node = node.nxt
				i += 1
			if node != None:
				del node.nxt
				
	def __init__(self, N, tabu=None, tabuLength=18, *args, **kwargs):
		super(TabuLSSudoku, self).__init__(N, *args, **kwargs)
		if tabu != None:
			self.tabu = tabu
		else:
			self.tabu = self.TabuList(tabuLength)
			
	def copy(self, *args, **kwargs):
		return super(TabuLSSudoku, self).copy(tabu=self.tabu, *args, **kwargs) # Pass along the TabuLSSudoku specific data

	def solve(self, stepsAmnt=100000):
		""" Generates a random successor for the given state """

		# statistics
		self.visitedStatesTotal = 0
		self.visitedStates = {}
		times = 0

		# Variables used to determne the best successor
		bestHeur, optimum = self.copy().hillClimb(stepsAmnt=stepsAmnt)

		# STATISTICS
		# output the amount of states visited
		#print self.visitedStates
		p=0
		for q in self.visitedStates:
			p += self.visitedStates[q]
		print p
		print bestHeur, optimum.heuristicValue()
		print ""
		if bestHeur == 0:
			print("We found a solution in {} times!".format(restart))

		return optimum

	def hillClimb(self, stepsAmnt=100000):
		""" Hillclimbs until it finds a (local) maximum """
		curr = self.copy()
		currHeur = 20000 # Higher than the highest possible in a 9^2x9^2 puzzle
		best = curr.copy()
		bestHeur = best.heuristicValue()
		
		for i in range(stepsAmnt):
			currHeur, curr = curr.getBestNeighbour(exclusion=list(self.tabu.items()))
			if currHeur < bestHeur:
				best = curr.copy()
				bestHeur = currHeur
		return bestHeur, best
		
	def getBestNeighbour(self, exclusion=[]):
		""" Generates and checks all possible successor states and returns the best.
		The order in which it will check is the blocks left to right and top to bottom
		and within the block left to right and top to bottom. 
		 """
		bestSuccessor = self
		bestHeur = 20000 # Higher than the highest possible in a 9^2x9^2 puzzle
		for heur, succ in self.generateNeighbours(exclusion=exclusion):
			if heur < bestHeur:
				bestSuccessor = succ()
				if heur == bestHeur - 4:
					bestHeur = heur
					break
				bestHeur = heur
		return bestHeur, bestSuccessor
		
	def swap(self, sq1=None, sq2=None, *args, **kwargs):
		super(TabuLSSudoku, self).swap(sq1=sq1, sq2=sq2, *args, **kwargs)
		self.tabu.add((sq1, sq2))
		return self


if __name__ == "__main__":
	def parse_3_grid(grid):
		"""Convert grid to a TabuLSSudoku(3), or return False if a contradiction
		is detected."""
		su = TabuLSSudoku(3)
		values = {}
		for i in range(len(grid)):
			if grid[i] not in "0.":
				y, x = divmod(i, 9)
				values[su.xy2sq(x, y)] = int(grid[i])
		su = TabuLSSudoku.fromVals(3, values)
		return su

	grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
	grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
	
	global tabu
	sud = TabuLSSudoku(3)
	print(sud)
	
	def testGenerateNeighbours(su, n):
		for _ in range(n):
			for g in su.generateNeighbours():
				pass
				
	
	
	sud = parse_3_grid(grid2)
	print(sud)
	#sud.solve(restarts=1000, randomWalk=9)
	cProfile.run('print(sud.solve(stepsAmnt=10000))')
	#cProfile.run('testGenerateNeighbours(sud, 10000)')
