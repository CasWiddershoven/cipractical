#!/usr/bin/env python3
from copy import copy

def test(su, verbose=False):
    "A set of tests that must pass."
    assert len(su.squares) == su.N**4 # N**4
    assert len(su.unitlist) == 3*su.N**2 # 3*N**2
    assert all(len(su.units[s]) == 3 for s in su.squares)
    assert all(len(su.peers[s]) == 3*su.N**2-2*su.N-1 for s in su.squares) # 3*N**2-2*N-1
    
class Sudoku(object):
	def __init__(self, N, values=None, digits=None, squares=None, unitlist=None, units=None, peers=None, *args, **kwargs):
		self.N = N
		if digits:
			self.digits = digits
		else:
			self.digits = range(1, self.N**2+1)
		if squares:
			self.squares = squares
		else:
			self.squares = [(1 << (self.N**2+c)) + (1<<r)
									for c in range(self.N**2)
									for r in range(self.N**2)] # Now the row number of square i is log(self.squares[i] >> N**2)/log(2) and the column number is log(self.squares[i] & (1 << N**2 -1))/log(2)
		if unitlist:
			self.unitlist = unitlist
		else:
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
		if units:
			self.units = units
		else:
			self.units = dict((s, [u for u in self.unitlist if s in u]) for s in self.squares)
		if peers:
			self.peers = peers
		else:
			self.peers = dict((s, set(sum(self.units[s], [])) - set([s])) for s in self.squares)

		if values:
			self.values = values
		else:
			self.values = dict((s, 0) for s in self.squares)

	def copy(self, *args, **kwargs):
		su = self.__class__(self.N,  # self.__class__ so that it supports subclassing
							values=copy(self.values),
							digits=self.digits,
							squares=self.squares, 
							unitlist=self.unitlist, 
							units=self.units, 
							peers=self.peers, *args, **kwargs) # Reference the squares, unitlist, units and peers for performance improvement
		return su

	@classmethod
	def fromVals(cls, vals, N):
		su = cls(N)
		for key in vals:
			su.values[key] = vals[key]
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
		
	def equals(self, other):
		return self.values == other.values

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
		x, y = divmod(sq, 1<<(self.N**2))
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
