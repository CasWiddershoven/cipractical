#!/usr/bin/env python3

def test(su, verbose=False):
    "A set of tests that must pass."
    assert len(su.squares) == su.N**4 # N**4
    assert len(su.unitlist) == 3*su.N**2 # 3*N**2
    assert all(len(su.units[s]) == 3 for s in su.squares)
    assert all(len(su.peers[s]) == 3*su.N**2-2*su.N-1 for s in su.squares) # 3*N**2-2*N-1
    
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
			res += "".join("{:^{w}}".format(self.__strval__(self.getValue(x=c, y=r)), w=width) + ("|" if (c+1) % self.N == 0 and c < self.N**2 - 1 else '')
							for c in range(self.N**2)) + "\n"
			if (r+1) % self.N == 0 and r < self.N**2 - 1: res += line + "\n"
		res += "\n"
		return res

	def setValue(self, d, x=None, y=None, sq=None):
		if sq == None:
			sq = self.xy2sq(x, y)
		return self._setValue(d, sq)
		
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
		"""Converts a square coordinate to x, y coordinates, column and row
		coordinates"""
		x = sq & (sq - 1) # The first 1-bit in the bitstring sq
		y = sq - x # The other 1-bit in the bitstring sq
		x = x >> (self.N**2) # Shift x so that the coordinate of the 1 bit is the x coordinate
		xdec = 0
		ydec = 0
		while x > 1 or y > 1:
			if x:
				x = x >> 1
				xdec += 1
			if y:
				y = y >> 1
				ydec += 1
		return xdec, ydec

	def xy2sq(self, x, y):
		"""Converts x, y coordinates to the square coordinate (the key of
		the values dict"""
		return (1<<(self.N**2+x))+(1<<y)


if __name__ == "__main__":
	sud = Sudoku(2)
	print(sud)
