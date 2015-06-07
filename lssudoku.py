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
