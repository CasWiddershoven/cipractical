from sudoku import Sudoku

class LSSudoku(Sudoku):
	def __init__(self, N, *args, **kwargs):
		super(LSSudoku, self).__init__(N, *args, **kwargs)

		self.fill()

	def fill(self):
		prefill = {513:4,514:2}
		for u in range(18,27):
		    for val in range(self.N**2):
		            self.setValue(val+1,0,0,self.unitlist[u][val])

		for u in prefill:
		    v = self.getValue(0,0,u)
		    s = self.units[u][2][prefill[u]-1]
		    self.setValue(prefill[u],0,0,u)
		    self.setValue(v,0,0,s)

	def switch(self, x1=None, x2=None, y1=None, y2=None, sq1=None, sq2=None):
		if sq1 == None:
			sq1 = self.xy2sq(x1, y1)
		if sq2 == None:
			sq2 = self.xy2sq(x2, y2)
		val1 = self.getValue(sq=sq1)
		val2 = self.getValue(sq=sq2)
		self.setValue(val2, sq=sq1)
		self.setValue(val1, sq=sq2)
