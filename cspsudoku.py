from sudoku import Sudoku

class CSPSudoku(Sudoku):
	def __init__(self, N, *args, **kwargs):
		super(CSPSudoku, self).__init__(N, *args, **kwargs)
		
		self.digits = (1 << (N**2)) - 1 # Think of it as bitstrings, this is a string of length N**2 with only 1s
		self.values = dict((s, self.digits) for s in self.squares)
		
	def _setValue(self, d, sq):
		other_values = self.getValue(sq=sq) & (self.digits - d)
		if all(self.eliminate((1<<d2), sq=sq) for d2 in range(self.N**2) if (1<<d2) <= other_values and (1<<d2) & other_values):
			return self
		else:
			return False

	def eliminate(self, d, x=None, y=None, sq=None):
		"""Eliminate d from values[s]; propagate when values or places <= 2.
		Return values, except return False if a contradiction is detected."""
		if sq == None:
			sq = self.xy2sq(x, y)
		if self.getValue(sq=sq) < d or not self.getValue(sq=sq) & d:
			return self ## Already eliminated
		self.values[sq] = self.getValue(sq=sq) & (self.digits - d)
		## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
		if self.getValue(sq=sq) == 0:
			return False ## Contradiction: removed last value
		elif (self.getValue(sq=sq) & (self.getValue(sq=sq) - 1)) == 0: # If there is only one option left (notice that self.values[s]-1 is equal to changing the least significant 1 bit to 0 (and changing all less significant bits to 1), so this won't be 0 if there is more than one 1 bit, and as we've checked for self.values[s] == 0 before, it can't be that, either.)
			d2 = self.getValue(sq=sq)
			if not all(self.eliminate(d2, sq=sq2) for sq2 in self.peers[sq]):
				return False
		## (2) If a unit u is reduced to only one place for a value d, then put it there.
		for u in self.units[sq]:
			dplaces = [sq2 for sq2 in u if self.getValue(sq=sq2) >= d and self.getValue(sq=sq2) & d] # Every place where d is still allowed
			if len(dplaces) == 0:
				return False ## Contradiction: no place for this value
			elif len(dplaces) == 1:
				# d can only be in one place in unit; assign it there
				if not self.setValue(d, sq=dplaces[0]):
					return False
		return self
		
	def __strval__(self, val):
		return " ".join(str(d + 1) for d in range(self.N**2) if 1 << d & val)
		
def solve(su):
	"Using depth-first search and propagation, try all possible values."
	def some(seq):
		"Return some element of seq that is true."
		for e in seq:
			if e: return e
		return False
			
	def countBits(num):
		c = 0
		while num: # Until there are no 1 bits left
			num &= (num - 1) # Remove the least significant 1 bit
			c += 1 # And increment the counter
		return c
		
	if su is False:
		return False ## Failed earlier
	if all((su.getValue(sq=sq) & (su.getValue(sq=sq) - 1)) == 0 for sq in su.squares): # If for all squares there is only one option left. See r49, in Sudoku.eliminate.
		return su ## Solved!
	## Chose the unfilled square s with the fewest possibilities
	_,sq = min((countBits(su.getValue(sq=sq)), sq) for sq in su.squares if countBits(su.getValue(sq=sq)) > 1)
	return some(solve(su.copy().setValue(1<<d, sq=sq))
				for d in range(su.N**2) if (1<<d) <= su.getValue(sq=sq) and (1<<d)&su.getValue(sq=sq))
   
def grid_values(grid, squares, digits, N=3):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [1<<(int(c)-1) if c not in '0.' else digits for c in grid if c in "0.123456789"]
    assert len(chars) == N**4
    return dict(zip(squares, chars))            
    
def parse_3_grid(grid):
	"""Convert grid to a CSPSudoku(3), or return False if a contradiction
	is detected."""
	su = CSPSudoku(3)
	values = dict((s, su.digits) for s in su.squares)
	for sq, d in grid_values(grid, su.squares, su.digits).items():
		x, y = su.sq2xy(sq)
		if d != su.digits and not su.setValue(d, sq=sq):
			return False
	return su

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
		
if __name__ == "__main__":
	sud = CSPSudoku(2)
	print(sud)
	print("\n\n")
	print(solve(parse_3_grid(grid1)))
	print(solve(parse_3_grid(grid2)))
	print(solve(parse_3_grid(hard1)))
