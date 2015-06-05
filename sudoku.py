#!/usr/bin/env python3

def test(su, verbose=False):
    "A set of tests that must pass."
    assert len(su.squares) == su.N**4 # N**4
    assert len(su.unitlist) == 3*su.N**2 # 3*N**2
    assert all(len(su.units[s]) == 3 for s in su.squares)
    assert all(len(su.peers[s]) == 3*su.N**2-2*su.N-1 for s in su.squares) # 3*N**2-2*N-1
    if verbose: print 'All tests pass.'
    
class Sudoku(object):
	def __init__(self, N, *args, **kwargs):

		self.N = N
		self.digits = range(1, self.N**2+1)
		self.squares = [(1 << (self.N**2+c)) + (1<<r) 
								for c in range(self.N**2) 
								for r in range(self.N**2)] # Now the row number of square i is log(self.squares[i] >> N**2)/log(2) and the column number is log(self.squares[i] & (1 << N**2 -1))/log(2)
		self.unitlist = ([[(1<<(self.N**2+c)) + (1<<r) 
							for r in range(self.N**2)] 
									for c in range(self.N**2)] +
					[[(1<<(self.N**2+c)) + (1<<r) 
							for c in range(self.N**2)] 
									for r in range(self.N**2)] +
					[[(1<<(self.N**2+c1*self.N + c2)) + (1<<(r1*self.N+r2)) 
							for r2 in range(self.N) 
							for c2 in range(self.N)] 
									for r1 in range(self.N) 
									for c1 in range(self.N)])
		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
		self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.squares)
		
		self.values = dict((s, 0) for s in self.squares)
		
		test(self)
		
	def copy(self):
		su = self.__class__(self.N) # Supports subclassing
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
		width = 2 + max(len(self.__strval__(self.getValue(sq=sq))) for sq in self.squares)
		line = '+'.join(['-'*(width*self.N)]*self.N)
		for r in range(self.N**2):
			res += "".join(" " + self.__strval__(self.getValue(x=c, y=r)) + " " + ("|" if (c+1) % self.N == 0 and c < self.N**2 - 1 else '')
							for c in range(self.N**2)) + "\n"
			if (r+1) % self.N == 0 and r < self.N**2 - 1: res += line + "\n"
		res += "\n"
		return res
		
	def setValue(self, d, x=None, y=None, sq=None):
		if sq == None:
			sq = self.xy2sq(x, y)
		self._setValue(self, d, sq)
		
	def _setValue(self, d, sq):
		self.values[sq] = d
		return self
		
	def getValue(self, x=None, y=None, sq=None):
		if sq == None:
			sq = self.xy2sq(x, y)
		return self.values[sq]
		
	def __strval__(self, val):
		return str(val)
		
	def sq2xy(self, sq):
		x = sq & (sq - 1) # The first 1-bit in the bitstring sq
		y = sq - x # The other 1-bit in the bitstring sq
		return x, y
		
	def xy2sq(self, x, y):
		return (1<<(self.N**2+x))+(1<<y)
		
class CSPSudoku(Sudoku):
	def __init__(self, N, *args, **kwargs):
		super(CSPSudoku, self).__init__(N, *args, **kwargs)
		
		self.digits = (1 << (N**2)) - 1 # Think of it as bitstrings, this is a string of length N**2 with only 1s
		self.values = dict((s, self.digits) for s in self.squares)
		
	def _assign(self, d, sq):
		other_values = self.values[sq] & (self.digits - d)
		if all(self.eliminate((1<<d2), sq=sq) for d2 in range(self.N**2) if (1<<d2) <= other_values and (1<<d2) & other_values):
			return self
		else:
			return False

	def eliminate(self, d, x=None, y=None, sq=None):
		"""Eliminate d from values[s]; propagate when values or places <= 2.
		Return values, except return False if a contradiction is detected."""
		if sq == None:
			sq = self.xy2sq(x, y)
		if self.values[sq] < d or not self.values[sq] & d:
			return self ## Already eliminated
		self.values[sq] = self.values[sq] & (self.digits - d)
		## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
		if self.values[sq] == 0:
			return False ## Contradiction: removed last value
		elif (self.values[sq] & (self.values[sq] - 1)) == 0: # If there is only one option left (notice that self.values[s]-1 is equal to changing the least significant 1 bit to 0 (and changing all less significant bits to 1), so this won't be 0 if there is more than one 1 bit, and as we've checked for self.values[s] == 0 before, it can't be that, either.)
			d2 = self.values[sq]
			if not all(self.eliminate(d2, sq=sq2) for sq2 in self.peers[sq]):
				return False
		## (2) If a unit u is reduced to only one place for a value d, then put it there.
		for u in self.units[sq]:
			dplaces = [sq2 for sq2 in u if self.values[sq] >= d and self.values[sq] & d] # Every place where d is still allowed
			if len(dplaces) == 0:
				return False ## Contradiction: no place for this value
			elif len(dplaces) == 1:
				# d can only be in one place in unit; assign it there
				if not self.assign(d, sq=dplaces[0]):
					return False
		return self
		
	def __strval__(self, val):
		return " " + " ".join(str(d + 1) for d in range(self.N**2) if 1 << d & val) + " "
		

#class Sudoku:
	#data = []
	#size = None
	
	#def __init__(self, data, n, *args, **kwargs):
		#self.data = data
		#self.size = n
	
	#def getBlock(self, i):
		#return [self.data[self.size*i+self.size**2*j+self.size*k] for j in range(self.size) for k in range(self.size)]
		
	#def getRow(self, i):
		#return [self.data[i*self.size**2 + j] for j in range(self.size**2)]
		
	#def getColumn(self, i):
		#return [self.data[i + j*self.size**2] for j in range(self.size**2)]
		
	#def __str__(self, *args, **kwargs):
		#string = ""
		#for i in range(self.size**2):
			#row = ["{:<4}".format(d) for d in self.getRow(i)]
			#for j in range(self.size, self.size**2, self.size):
				#row = row[:j + j / self.size - 1] + [" | "] + row[j + j / self.size - 1:]
			#string += "".join([str(j) for j in row])
			#string += "\n"
			#if (i + 1) % self.size == 0 and i != self.size**2 - 1:
				#string += "-"*(4 * self.size**2 + (self.size - 1) * 2)
				#string += "\n"
		#return string

if __name__ == "__main__":
	sud = CSPSudoku(2)
	print(sud)
