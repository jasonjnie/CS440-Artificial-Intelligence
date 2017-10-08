import sys
from copy import deepcopy

""" Read the Gird """
grid = [];
indX = 0;
indY = 0;
with open(sys.argv[1]) as f_grid:
	for line in f_grid:
		grid.append([]);
		indX = 0;
		for char in line:
			if char != '\n':
				grid[indY].append(char);
				indX+=1;
		indY+=1;

""" Read the bank """
bank = [];
with open(sys.argv[2]) as f_bank:
	for line in f_bank:
			bank.append([ char.upper() for char in line.splitlines()]); 

""" Use the hint """
grid_count = deepcopy(grid);
for y in range(len(grid)):
	for x in range(len(grid[0])):
		if grid[y][x] != '_':
			grid_count[y][x] = 1;
		else:
			grid_count[y][x] = 0;
assignment = [None]*(len(bank));

class CSP_backtracing:

	def __init__(self,grid,bank,assignment,grid_count):
		""" Constructor """
		self.grid = grid; 					  # '_' means no assignement yet
		self.bank = bank;
		self.assignment = assignment; # For example self.assignment[1] = ['V',1,1];
		self.height = len(grid);
		self.width = len(grid[0]);
		self.grid_count = grid_count;

	def select_unassigned_vaiable(self):
		curlen=0
		i = 0 #keep track of word in bank
		curvar = "";
		for word in bank:
			if self.assignment[i] == None:  # word has not been assigned 
				if len(word[0]) > curlen:
					curlen = len(word[0])
					curvar = word[0]
			i = i + 1
		return curvar #choose the longest word

	def order_domain_value(self,var):
		valuelist = []
		wordLength = len(var)

		for i in range (0, len(self.grid)-len(var)+1):
			for j in range (0, len(self.grid[0])):
				place = 'true'
				for k in range (i,i+len(var)):#this word's whole spots correct overlap
					if self.grid[k][j] != '_' :
						if self.grid[k][j] != var[k-i]:
							place = 'false'
				if place == 'true':					
					value = ['V',i,j]
					valuelist.append(value)
					
		for j in range (0, len(self.grid[0])-len(var)+1):
			for i in range (0, len(self.grid)):
				#every possible spot 
				place = 'true'
				for k in range (j,j+len(var)):#this word's whole spots correct overlap
					if self.grid[i][k] != '_' :
						if self.grid[i][k] != var[k-j]:
							place = 'false'
				if place == 'true':					
					value = ['H',i,j]
					valuelist.append(value)


		#all the possible values

		return valuelist


	def inference(self):
		return True;

	def consistent_vertical(self,grid,var,value):
		wordLength = len(var);
		curCols = [];
		xind = 0;
		yind = 0;
		for row in grid:
			if yind < value[1] and yind > (value[1] + wordLength - 1):
				curCols.append(row[value[2]]);
			yind += 1;
		""" Check all the rows"""
		for dy in range(wordLength):
			if var[dy] in (grid[value[1]+dy][0:value[2]] + grid[value[1]+dy][value[2]+1:]):
				return False;
		for dx in range(len(curCols)):
			if curCols[dx] in var:
				return False;
		firstBox = value[1]//3;
		lastBox = (value[1]+ wordLength-1)//3;
		bx = value[2]//3;
		for by in range(firstBox,lastBox+1):
			curBox = [];
			if by == firstBox:
				for i in range(by*3,by*3+3):
					for j in range(bx*3,bx*3+3):
						if i < value[1] or j != value[2]:
							curBox.append(grid[i][j]);
				for i in range(value[1],by*3+3):
					if var[i-value[1]] in curBox:
						return False;
			elif by == lastBox:
				for i in range(by*3,by*3+3):
					for j in range(bx*3,bx*3+3):
						if i > (value[1] + wordLength - 1) or j != value[2]:
							curBox.append(grid[i][j]);
				for i in range(by*3,(value[1] + wordLength - 1)):
					if var[i-value[1]] in curBox:
						return False;
			else:
				for i in range(by*3,by*3+3):
					for j in range(bx*3,bx*3+3):
						if j != value[2]:
							curBox.append(grid[i][j]);
				for i in range(by*3,by*3+3):
					if var[i-value[1]] in curBox:
						return False;
		return True;

	def is_consistent(self,var,value):
		if value[0] == 'V':
			return self.consistent_vertical(self.grid,var,value);
		else:
			grid_trans = [];
			for y in range(self.width):
				temp = [];
				for x in range(self.height):
					temp.append(self.grid[x][y]);
				grid_trans.append(list(temp));
			return self.consistent_vertical(grid_trans,var,['V',value[2],value[1]]);

	def is_complete(self):
		""" Check to see if the grid has been completely filled """
		for line in self.grid:
			for char in line:
				if char == '_':
					return False;
		return True;

	def remove_assignemt(self,var,value):
		ind = 0;
		for word in self.bank:
			if word[0] == var:
				self.assignment[ind] = -1;
			ind += 1;
		wordLength = len(var);
		if value[0] == 'V':
			for dx in range(wordLength):
				self.grid_count[value[1]+dx][value[2]] -= 1;
				if self.grid_count[value[1]+dx][value[2]] == 0:
					self.grid[value[1]+dx][value[2]] = '_';
		else:
			for dx in range(wordLength):
				self.grid_count[value[1]][value[2]+dx] -= 1;
				if self.grid_count[value[1]][value[2]+dx] == 0:
					self.grid[value[1]][value[2]+dx] = '_';

	def add_assignment(self,var,value):
		ind = 0;
		for word in self.bank:
			if word[0] == var:
				self.assignment[ind] = value;
			ind += 1;
		wordLength = len(var);
		if value[0] == 'V':
			for dy in range(wordLength):
				self.grid[value[1]+dy][value[2]] = var[dy];
				self.grid_count[value[1]+dy][value[2]] += 1;
		else:
			for dx in range(wordLength):
				self.grid[value[1]][value[2]+dx] = var[dx];		
				self.grid_count[value[1]][value[2]+dx] += 1;	

	def display(self):
		for row in self.grid:
			rowString = "";
			for char in row:
				rowString += char;
			print(rowString);

def display(grid):
	for row in grid:
		rowString = "";
		for char in row:
			rowString += char;
		print(rowString);

""" Top csp backtracing search level """
LIST = []
def recursive_backtracing(grid,bank,assignment,grid_count):
	search = CSP_backtracing(grid,bank,assignment,grid_count);
	global node
	"""
	if search.is_complete():
		return search;
	"""

	var = search.select_unassigned_vaiable();
	if var == "":
		return search;

	valuelist = search.order_domain_value(var)
	assignment_temp = deepcopy(search.assignment);

	for value in valuelist:
		node += 1;
		if search.is_consistent(var,value):
			if search.inference():
				search.add_assignment(var,value)
				search = deepcopy(recursive_backtracing(search.grid,search.bank,deepcopy(search.assignment),search.grid_count));
				if search.is_complete():
					LIST.append([var,value])
					return search;
				else:
					search.remove_assignemt(var,value);
					search.assignment = assignment_temp;
	return search;

"""
node = 0;
search = recursive_backtracing(grid,bank,assignment,grid_count)
search.display();
print(node)
#print(search.assignment);
for x in range(len(LIST)-1,-1,-1):
	print(LIST[x][1],":",LIST[x][0])
"""
LIST = [[['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], -1, ['V', 4, 4], ['V', 5, 8], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]]
[[['V', 0, 0], ['V', 5, 8], -1, ['H', 3, 4], ['H', 7, 3], ['V', 4, 4], ['V', 5, 6], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 8], -1, ['H', 3, 4], ['H', 7, 3], ['V', 4, 4], ['V', 5, 6], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], -1, -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], ['H', 7, 3], ['V', 4, 4], ['V', 5, 8], ['H', 5, 5], ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], ['H', 7, 3], ['V', 4, 4], ['V', 5, 8], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], ['H', 7, 3], ['V', 4, 4], ['V', 5, 8], ['H', 5, 5], ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], -1, -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], ['H', 7, 3], ['V', 4, 4], ['V', 5, 8], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], -1, -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 8], -1, ['H', 3, 4], -1, ['V', 4, 4], ['V', 5, 6], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], -1, ['V', 4, 4], ['V', 5, 8], ['H', 5, 5], ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]], [['V', 0, 0], ['V', 5, 6], -1, ['H', 3, 4], -1, ['V', 4, 4], ['V', 5, 8], -1, ['V', 5, 5], ['V', 0, 1], ['H', 2, 2], ['H', 0, 1], ['H', 7, 0], -1, ['V', 6, 0], ['H', 4, 5], ['V', 3, 3], ['V', 5, 7], ['V', 1, 2], ['H', 8, 2], ['H', 1, 1]]]
]

print(len(LIST))


