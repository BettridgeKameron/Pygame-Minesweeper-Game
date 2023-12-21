from numpy import pad
import secrets

class MineSweeperLogic:
	height = 5
	width = 5
	def __init__(self, height, width):
		self.height = height
		self.width = width
		self.grid = pad([[0 for y in range(width)] for x in range(height)], pad_width=1, mode='constant', constant_values=-1) #note: the grid has a 1 long buffer zone arround it on all sides to prevent out of bounds errors
		self.clickGrid = pad([[0 for y in range(width)] for x in range(height)], pad_width=1, mode='constant', constant_values=-1)
		self.flagGrid = pad([[0 for y in range(width)] for x in range(height)], pad_width=1, mode='constant', constant_values=-1)
	#pre-condition: mines<height*length, grid is empty
	def generateMines(self,grid,mines):
		coordList = [(x, y) for x in range(1,self.height+1) for y in range(1,self.width+1)]
		secrets.SystemRandom().shuffle(coordList)
		for coord in coordList[:mines]:
			grid[coord[0]][coord[1]] = 10
		
	def generateNums(self,grid):
		for x in range(1,self.height+1):
				for y in range(1,self.width+1):
					if grid[x][y] == 10:
						continue
					grid[x][y] = self.checkMineTot(grid,x,y)
	
	def checkMineTot(self,grid,x1,y1):
		mineCount = 0
		for x in range(-1,2):
			for y in range(-1,2):
				if x == y == 0:
					continue
				if grid[x1 + x][y1 + y] == 10:
					mineCount += 1
		return mineCount
