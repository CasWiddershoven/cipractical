#!/usr/bin/env python3

from sudoku import Sudoku
from random import randrange, shuffle
from copy import copy, deepcopy
import time, random

class LSSudoku(Sudoku):
	def __init__(self, N, values=None, prefill=None, possibleSwaps=None, *args, **kwargs):
		super(LSSudoku, self).__init__(N, values=values, *args, **kwargs)
		self.fill(values=values, prefill=prefill, possibleSwaps=possibleSwaps)
		
	def fill(self, file = None, values=None, prefill = None, possibleSwaps = None):
		""" Fills the sudoku with a pre-chosen list (can be read from file) and fills
		 in the rest with "random" numbers (1-9) """
		if prefill != None:
			self.prefill = prefill
		elif file == None:
			self.prefill = {}
		else:
			f = open('sudoku.txt')
			self.prefill = f.read()
			f.close()
			
		if possibleSwaps != None:
			self.possibleSwaps = possibleSwaps
		else:
			def getRowsAndColumns(square1, square2):
				x1, y1 = divmod(square1, 1<<(self.N**2))
				x2, y2 = divmod(square2, 1<<(self.N**2))
				if x1 != x2:
					col1 = [i for i in self.units[square1][0] if i != square1]
					col2 = [i for i in self.units[square2][0] if i != square2]
				else:
					col1 = col2 = False
				if y1 != y2:
					row1 = [i for i in self.units[square1][1] if i != square1]
					row2 = [i for i in self.units[square2][1] if i != square2]
				else:
					row1 = row2 = False
				
				return col1, row1, col2, row2
			self.possibleSwaps = [(self.unitlist[u][square1], self.unitlist[u][square2],
									getRowsAndColumns(self.unitlist[u][square1], self.unitlist[u][square2]))
										for square1 in range(self.N**2) 
										for square2 in range(square1, self.N**2) 
										for u in range(2*self.N**2, 3*self.N**2)
											if self.unitlist[u][square1] not in self.prefill and self.unitlist[u][square2] not in self.prefill]
		if values != None:
			self.values = values
		else:
			for u in range(2* self.N**2,3* self.N**2): # For each self.N x self.N block
				digits = [d for d in self.digits]
				for sq in self.unitlist[u]:
					if sq in self.prefill:
						self.setValue(self.prefill[sq], sq=sq)
						digits.remove(self.prefill[sq])
				shuffle(digits)
				for sq in self.unitlist[u]:
					if sq not in self.prefill:
						self.setValue(digits.pop(), sq=sq)
			
	@classmethod
	def fromVals(cls, N, vals):
		sud = cls(N)
		sud.fill(prefill=vals)
		return sud
		
	def copy(self, *args, **kwargs):
		return super(LSSudoku, self).copy(prefill=self.prefill, possibleSwaps=self.possibleSwaps, *args, **kwargs) # Pass along the local search specific data

	def swap(self, x1=None, y1=None, x2=None, y2=None, sq1=None, sq2=None):
		""" Swaps the values of 2 squares """
		if sq1 == None:
			sq1 = self.xy2sq(x1, y1)
		if sq2 == None:
			sq2 = self.xy2sq(x2, y2)
		val1 = self.values[sq1]
		val2 = self.values[sq2]

		self.values[sq1] = val2
		self.values[sq2] = val1
		return self

	def heuristicValue(self):
		""" Calculates the heursitc value of the sudoku """
		_sum = 0

		for u in self.unitlist[:2 * self.N**2]: # Check only the rows and columns; the blocks should be good
			nums = [1] * self.N**2
			for sq in u:
				nums[self.getValue(sq=sq) - 1] = 0
			_sum += sum(nums) # Nums now is 1 on all the places where there was no square containing the value and 0 on all others
		return _sum
		
	def generateNeighbours(self, exclusion=[]):
		""" An iterator that generates all neighbours """
		heur = self.heuristicValue()
		possibleSwaps = filter(lambda (sq1, sq2, _): (sq1, sq2) not in exclusion, self.possibleSwaps)
		for sq1, sq2, (col1, row1, col2, row2) in possibleSwaps:
			d = 0
			val1 = self.values[sq1]
			val2 = self.values[sq2]
			if col1:
				col1 = [self.values[sq] for sq in col1]
				if val1 in col1:
					d -= 1
				if val2 in col1:
					d += 1
			if col2:
				col2 = [self.values[sq] for sq in col2]
				if val1 in col2:
					d += 1
				if val2 in col2:
					d -= 1
			if row1:
				row1 = [self.values[sq] for sq in row1]
				if val1 in row1:
					d -= 1
				if val2 in row1:
					d += 1
			if row2:
				row2 = [self.values[sq] for sq in row2]
				if val1 in row2:
					d += 1
				if val2 in row2:
					d -= 1
			
			yield heur + d, lambda: self.copy().swap(sq1=sq1, sq2=sq2)

	def getBestNeighbour(self):
		""" Generates and checks all possible successor states and returns the best.
		The order in which it will check is the blocks left to right and top to bottom
		and within the block left to right and top to bottom. 
		 """
		bestSuccessor = self
		bestHeur = 20000 # Higher than the highest possible in a 9^2x9^2 puzzle
		for heur, succ in self.generateNeighbours():
			if heur < bestHeur:
				bestSuccessor = succ() # Weird... We somehow must generate each next bestSuccessor for the algorithm to work, instead of only the final best.
				if heur == bestHeur - 4:
					bestHeur = heur
					break
				bestHeur = heur

		return bestHeur, bestSuccessor


if __name__ == "__main__":
	sud = LSSudoku(3)
	print(sud)
	print(sud.heuristicValue())
	it = sud.generateNeighbours()
	#it.next()
	print(it.next())

	def switch(self, x1=None, x2=None, y1=None, y2=None, sq1=None, sq2=None):
		if sq1 == None:
			sq1 = self.xy2sq(x1, y1)
		if sq2 == None:
			sq2 = self.xy2sq(x2, y2)
		val1 = self.getValue(sq=sq1)
		val2 = self.getValue(sq=sq2)
		self.setValue(val2, sq=sq1)
		self.setValue(val1, sq=sq2)
