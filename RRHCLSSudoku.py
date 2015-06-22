from lssudoku import LSSudoku
from random import randrange, shuffle
import copy, time, random, cProfile

class RRHCLSSudoku(LSSudoku):
	def __init__(self, N, *args, **kwargs):
		super(RRHCLSSudoku, self).__init__(N, *args, **kwargs)
		
	def solve(self, restarts=1000):
		curr = self.copy()
		optimum = curr
		bestHeur = 20000 # Higher than the highest possible in a 9^2x9^2 puzzle
		for r in range(restarts):
			currHeur, curr = curr.hillClimb()
			if currHeur < bestHeur:
				optimum = curr
				if bestHeur == 0:
					print("Found a solution in {} times!".format(r))
					return optimum
			curr = curr.randomRestart()
		print("No solution found in {} times".format(restarts))
		return optimum
		
	def randomRestart(self):
		nxt = self.copy()
		for u in range(2* self.N**2,3* self.N**2): # For each self.N x self.N block
			digits = [d for d in self.digits]
			for sq in self.unitlist[u]:
				if sq in self.prefill:
					nxt.setValue(self.prefill[sq], sq=sq)
					digits.remove(self.prefill[sq])
			shuffle(digits)
			for sq in self.unitlist[u]:
				if sq not in self.prefill:
					nxt.setValue(digits.pop(), sq=sq)
		return nxt

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

if __name__ == "__main__":
	def parse_3_grid(grid):
		"""Convert grid to a ILSSudoku(3), or return False if a contradiction
		is detected."""
		su = RRHCLSSudoku(3)
		values = {}
		for i in range(len(grid)):
			if grid[i] not in "0.":
				y, x = divmod(i, 9)
				values[su.xy2sq(x, y)] = int(grid[i])
		su = RRHCLSSudoku.fromVals(3, values)
		return su

	grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
	grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
	hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
	
	
	sud = RRHCLSSudoku(3)
	print(sud)
	
	sud = parse_3_grid(grid2)
	print(sud)
	cProfile.run('print(sud.solve())')
