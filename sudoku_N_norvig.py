## Solve Every Sudoku Puzzle

## See http://norvig.com/sudoku.html

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

from math import log

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]
    
class Sudoku:
	def __init__(self, N):
		self.N = N
		self.rows = self.cols = self.digits = 2**(N**2)-1 # Think of it as bitstrings, this is a string of length N**2 with only 1s
		self.squares = [(1 << (N**2+c)) + (1<<r) for c in range(N**2) for r in range(N**2)] # Now the row number of square i is log(self.squares[i] >> N**2)/log(2) and the column number is log(self.squares[i] & (1 << N**2 -1))/log(2)
		self.unitlist = ([[(1<<(N**2+c)) + (1<<r) for r in range(N**2)] for c in range(N**2)] +
					[[(1<<(N**2+c)) + (1<<r) for c in range(N**2)] for r in range(N**2)] +
					[[(1<<(N**2+c1*N + c2)) + (1<<(r1*N+r2)) for r2 in range(N) for c2 in range(N)] for r1 in range(N) for c1 in range(N)])
		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
		self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.squares)
		
		self.values = dict((s, self.digits) for s in self.squares)
		
		test(self)
		
	def assign(self, s, d):
		other_values = self.values[s] & (self.digits - d)
		if all(self.eliminate(s, (1<<d2)) for d2 in range(self.N**2) if (1<<d2) <= other_values and (1<<d2)&other_values):
			return self
		else:
			return False

	def eliminate(self, s, d):
		"""Eliminate d from values[s]; propagate when values or places <= 2.
		Return values, except return False if a contradiction is detected."""
		if self.values[s] < d or not self.values[s]&d:
			return self ## Already eliminated
		self.values[s] = self.values[s]&(self.digits - d)
		## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
		if self.values[s] == 0:
			return False ## Contradiction: removed last value
		elif (self.values[s] & (self.values[s] - 1)) == 0: # If there is only one option left (notice that self.values[s]-1 is equal to changing the least significant 1 bit to 0 (and changing all less significant bits to 1), so this won't be 0 if there is more than one 1 bit, and as we've checked for self.values[s] == 0 before, it can't be that, either.)
			d2 = self.values[s]
			if not all(self.eliminate(s2, d2) for s2 in self.peers[s]):
				return False
		## (2) If a unit u is reduced to only one place for a value d, then put it there.
		for u in self.units[s]:
			dplaces = [s for s in u if self.values[s] >= d and self.values[s]&d] # Every place where d is still allowed
			if len(dplaces) == 0:
				return False ## Contradiction: no place for this value
			elif len(dplaces) == 1:
				# d can only be in one place in unit; assign it there
				if not self.assign(dplaces[0], d):
					return False
		return self
		
	def copy(self):
		su = Sudoku(self.N)
		su.values = self.values.copy()
		test(su)
		return su
		
	@staticmethod
	def from_vals(vals, N):
		su = Sudoku(N)
		for key in vals:
			su.values[key] = vals[key]
		test(su)
		return su
		
	def __str__(self):
		res = ""
		width = 3 + max((1 + len(str(self.N**2)))*countBits(self.values[s]) for s in self.squares)
		line = '+'.join(['-'*(width*self.N)]*self.N)
		res += "+" + line + "+" + "\n"
		for r in range(self.N**2):
			res += "|" + "".join(["".join(str(i) for i in getBits(self.values[(1<<(self.N**2 + c)) + (1<<r)])).center(width)+('|' if (c+1) % self.N == 0 else '')
                      for c in range(self.N**2)]) + "\n"
			if (r+1) % self.N == 0: res += "+" + line + "+" + "\n"
		res += "\n"
		return res

def test(su, verbose=False):
    "A set of tests that must pass."
    assert len(su.squares) == su.N**4 # N**4
    assert len(su.unitlist) == 3*su.N**2 # 3*N**2
    assert all(len(su.units[s]) == 3 for s in su.squares)
    assert all(len(su.peers[s]) == 3*su.N**2-2*su.N-1 for s in su.squares) # 3*N**2-2*N-1
    if verbose: print 'All tests pass.'

################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected."""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assign(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    return values
    
def parse_3_grid(grid):
	"""Convert grid to a Sudoku(3), or return False if a contradiction
	is detected."""
	su = Sudoku(3)
	values = dict((s, su.digits) for s in su.squares)
	for s, d in grid_values(grid, su.squares, su.digits).items():
		if d != su.digits and not su.assign(s, d):
			return False
	return su

def grid_values(grid, squares, digits, N=3):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [1<<(int(c)-1) if c not in '0.' else digits for c in grid if c in "0.123456789" or c in '0.']
    assert len(chars) == N**4
    return dict(zip(squares, chars))

################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False

def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values

################ Display as 2-D grid ################

def display(values, squares, rows, ret=False):
    "Display these values as a 2-D grid."
    res = ""
    width = 1+max(countBits(values[s]) for s in squares)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        res += ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols) + "\n"
        if r in 'CF': res += line + "\n"
	res += "\n"
	if not ret:
		print res
	else:
		return res

################ Search ################

def solve(grid): return search(parse_3_grid(grid))

def search(su):
    "Using depth-first search and propagation, try all possible values."
    if su is False:
        return False ## Failed earlier
    if all((su.values[s] & (su.values[s] - 1)) == 0 for s in su.squares): # If for all squares there is only one option left. See r49, in Sudoku.eliminate.
        return su ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((countBits(su.values[s]), s) for s in su.squares if countBits(su.values[s]) > 1)
    return some(search(su.copy().assign(s, 1<<d))
                for d in range(su.N**2) if (1<<d) <= su.values[s] and (1<<d)&su.values[s])

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return file(filename).read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq
    
def countBits(num):
	c = 0
	while num: # Until there are no 1 bits left
		num &= (num - 1) # Remove the least significant 1 bit
		c += 1 # And increment the counter
	return c
	
def getBits(num):
	c = []
	from math import log
	while num:
		num2 = num
		num2 &= (num - 1)
		c.append(log((num^(num-1))+1)/log(2))
		num = num2
	return c

################ System test ################

import time, random

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print '(%.2f seconds)\n' % t
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 1:
        print "Solved %d of %d %s puzzles (avg %.2f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

def random_puzzle(N=17):
    """Make a random puzzle with N or more assignments. Restart on contradictions.
    Note the resulting puzzle is not guaranteed to be solvable, but empirically
    about 99.8% of them are solvable. Some have multiple solutions."""
    values = dict((s, digits) for s in squares)
    for s in shuffled(squares):
        if not assign(values, s, random.choice(values[s])):
            break
        ds = [values[s] for s in squares if len(values[s]) == 1]
        if len(ds) >= N and len(set(ds)) >= 8:
            return ''.join(values[s] if len(values[s])==1 else '.' for s in squares)
    return random_puzzle(N) ## Give up and make a new puzzle

grid1  = '003020600900305001001806400008102900700000008006708200002609500800203009005010300'
grid2  = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
hard1  = '.....6....59.....82....8....45........3........6..3.54...325..6..................'
    
if __name__ == '__main__':
    #test()
    #solve_all(from_file("easy50.txt", '========'), "easy", None)
    #solve_all(from_file("top95.txt"), "hard", None)
    #solve_all(from_file("hardest.txt"), "hardest", None)
    #solve_all([random_puzzle() for _ in range(99)], "random", 100.0)
    print(solve(grid1))
    solve(grid2)

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
