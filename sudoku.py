#!/usr/bin/env python3

class Sudoku:
	data = []
	size = None
	
	def __init__(self, data, n, *args, **kwargs):
		self.data = data
		self.size = n
	
	def getBlock(self, i):
		return [self.data[self.size*i+self.size**2*j+self.size*k] for j in range(self.size) for k in range(self.size)]
		
	def getRow(self, i):
		return [self.data[i*self.size**2 + j] for j in range(self.size**2)]
		
	def getColumn(self, i):
		return [self.data[i + j*self.size**2] for j in range(self.size**2)]
		
	def __str__(self, *args, **kwargs):
		string = ""
		for i in range(self.size**2):
			row = ["{:<4}".format(d) for d in self.getRow(i)]
			for j in range(self.size, self.size**2, self.size):
				row = row[:j + j / self.size - 1] + [" | "] + row[j + j / self.size - 1:]
			string += "".join([str(j) for j in row])
			string += "\n"
			if (i + 1) % self.size == 0 and i != self.size**2 - 1:
				string += "-"*(4 * self.size**2 + (self.size - 1) * 2)
				string += "\n"
		return string

if __name__ == "__main__":
	sud = Sudoku(range(3**4), 3)
	print(sud)
