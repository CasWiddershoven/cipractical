from lssudoku import LSSudoku
from random import sample
import cProfile

class ILSSudoku(LSSudoku):
	def __init__(self, N, *args, **kwargs):
		super(ILSSudoku, self).__init__(N, *args, **kwargs)

	def solve(self, restarts=3, randomWalk=1):
		""" Generates a random successor for the given state """

		# statistics
		self.visitedStatesTotal = 0
		self.visitedStates = {}
		times = 0

		# Variables used to determne the best successor
		bestHeur, optimum = self.copy().hillClimb()

		for restart in range(restarts):
			curr = optimum.randomWalk()
			currHeur, curr = curr.hillClimb()
			if currHeur < bestHeur:
				optimum = curr
				bestHeur = currHeur
				if bestHeur == 0:
					times = restart
					break

			# STATISTICS
			self.visitedStates[restart] = self.visitedStatesTotal
			self.visitedStatesTotal = 0

		# STATISTICS
		# output the amount of states visited
		#print self.visitedStates
		p=0
		for q in self.visitedStates:
			p += self.visitedStates[q]
		print p
		print bestHeur
		print ""
		if bestHeur == 0:
			print("We found a solution in {} times!".format(restart))

		return optimum

	def hillClimb(self, plateauSize=3):
		""" Hillclimbs until it finds a (local) maximum """
		curr = self.copy()
		currHeur = 20000 # Higher than the highest possible in a 9^2x9^2 puzzle
		
		localMaximum = False # do ... while emulation
		timeOnPlateau = plateauSize
		while not localMaximum:
			bestHeur, bestSucc = curr.getBestNeighbour()
			if bestHeur < currHeur:
				curr = bestSucc
				currHeur = bestHeur
				timeOnPlateau = plateauSize
				if bestHeur == 0: # We did it! We finished the sudoku!
					return bestHeur, bestSucc
			elif timeOnPlateau and bestHeur == currHeur:
				timeOnPlateau -= 1 # timeOnPlateau decreases until it's 0 from the max time it may be on a plateau, namely plateauSize
				curr = bestSucc
			else:
				localMaximum = True
		return bestHeur, bestSucc


	def randomWalk(self, amount=4):
		""" Does an "amount" amount of random steps """ 
		curr = self.copy()
		for sq1, sq2, _ in sample(curr.possibleSwaps, amount):
			curr.swap(sq1=sq1, sq2=sq2) # Do a random step

		return curr


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
		su = ILSSudoku.fromVals(3, values)
		return su

	grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
	grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
	
	
	sud = ILSSudoku(3)
	print(sud)
	
	def testGenerateNeighbours(su, n):
		for _ in range(n):
			for g in su.generateNeighbours():
				pass
				
	
	
	sud = parse_3_grid(grid2)
	print(sud)
	#sud.solve(restarts=1000, randomWalk=9)
	cProfile.run('sud.solve(restarts=2000, randomWalk=20)')
	#cProfile.run('testGenerateNeighbours(sud, 10000)')
