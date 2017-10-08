# -*- coding: utf-8 -*-
from queue import *
import sys


""" Maze Class """
class Maze_One_Dot:
	""" Maze class for one dot """
	def __init__(self,maze):
		self.maze = maze;
		self.size = [self.getHeight(maze),self.getWidth(maze)];
		self.start = self.find_start(maze);
		self.end = self.find_end(maze);
	def find_start(self,maze):
		""" The function to find the starting state and return a list of coordinates"""
		x_ind = 0;
		y_ind = 0;
		for line in maze:
			x_ind = 0;
			for char in line:
				if char == 'P':
					return [y_ind,x_ind];
				x_ind += 1;
			y_ind += 1;

	def find_end(self,maze):
		""" The function to find the starting state and return a list of coordinates"""
		x_ind = 0;
		y_ind = 0;
		for line in maze:
			x_ind = 0;
			for char in line:
				if char == '.':
					return [y_ind,x_ind];
				x_ind += 1;
			y_ind += 1;

	def is_goal(self,state):
		""" Goal of the 1.1 """
		if state[0] == self.end[0] and state[1] == self.end[1]:
			return True;
		else:
			return False;

	def getWidth(self,maze):
		return len(maze[0]);
	def getHeight(self,maze):
		return len(maze);
	def is_legal(self,point):
		if point[0] >= 0 and point[0] < self.size[0]:
			if point[1] >= 0 and point[1] < self.size[1]:
				if self.maze[point[0]][point[1]] != '%':
					return True;
		return False;
	def draw(self,point,char):
		self.maze[point[0]][point[1]] = char;
	def display(self):
		for line in self.maze:
			for char in line:
				print(char,end="");
			print('\n')

	
""" All the search method class """
class BFS_Search_Maze_Unique:
	""" BFS Search for the maze with only one dot"""
	def __init__(self,maze):
		self.frontier = Queue();
		self.maze = Maze_One_Dot(maze);
		self.start = self.maze.start;
		self.frontier.put(self.start);
		self.explored = [];
		self.end = self.maze.end;
		self.parent = {};
		self.path_cost = 0

	def is_end(self,state):
		return self.maze.is_goal(state);

	def is_empty(self):
		return self.frontier.empty();

	def next_nodes(self):
		return self.frontier.get();

	def get_end(self):
		return self.maze.end;

	def expand(self,state):
		new_state = list(state);
		new_state[0] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.put(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
		new_state = list(state);
		new_state[0] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.put(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
		new_state = list(state);
		new_state[1] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.put(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
		new_state = list(state);
		new_state[1] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.put(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;

	def draw_path(self,end):
		self.path_cost += 1
		if end == self.start[0:2]:
			return;
		self.maze.draw(end,'.');
		self.draw_path(self.parent[','.join(str(v) for v in end)]);
	def display(self):
		self.maze.display();


class DFS_Search_Maze_Unique(BFS_Search_Maze_Unique):
	""" DFS Search for the maze with only one dot"""
	def __init__(self,maze):
		self.frontier = [];
		self.maze = Maze_One_Dot(maze);
		self.start = self.maze.start;
		self.end = self.maze.end;
		self.frontier.append(self.start);
		self.explored = [];
		self.parent = {};	
		self.path_cost = 0

	def is_empty(self):
		if len(self.frontier) == 0:
			return True;
		else:
			return False;

	def next_nodes(self):
		return self.frontier.pop();

	def expand(self,state):
		new_state = list(state);
		new_state[0] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.append(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
		new_state = list(state);
		new_state[0] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.append(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
		new_state = list(state);
		new_state[1] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.append(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
		new_state = list(state);
		new_state[1] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.frontier.append(new_state);
				self.explored.append(new_state);
				self.parent[','.join(str(v) for v in new_state)] = state;
	 
class Greedy_Search_Maze_Unique(DFS_Search_Maze_Unique):
	""" Greedy Search for the maze with only one dot"""
	def _heuristic(self,state):
		return abs(state[0]-self.end[0])+abs(state[1]-self.end[1]);
	def expand(self,state):
		cur_heu_list = [];
		new_state = list(state);
		new_state[0] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:				
				new_state.append(self._heuristic(new_state));
				cur_heu_list.append(new_state);
				
		new_state = list(state);
		new_state[0] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:				
				new_state.append(self._heuristic(new_state));
				cur_heu_list.append(new_state);
				
		new_state = list(state);
		new_state[1] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				new_state.append(self._heuristic(new_state));
				cur_heu_list.append(new_state);
				
		new_state = list(state);
		new_state[1] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:				
				new_state.append(self._heuristic(new_state));
				cur_heu_list.append(new_state);
				
		if len(cur_heu_list) == 0:
			return;
		sorted_new_list = sorted(cur_heu_list,key= lambda x:x[2],reverse=True);
		for cur_state in sorted_new_list:
			self.parent[','.join(str(v) for v in cur_state[0:2])] = state;
			self.frontier.append(cur_state[0:2]);
			self.explored.append(cur_state[0:2]);
	
class A_Search_Maze_Unique(DFS_Search_Maze_Unique):

	def _heuristic(self,state):
		return abs(state[0]-self.end[0])+abs(state[1]-self.end[1]);
	def __init__(self,maze):
		self.frontier = [];
		self.maze = Maze_One_Dot(maze);
		self.start = self.maze.start;
		self.cur_dist = {};
		self.cur_dist[','.join(str(v) for v in self.start[0:2])] = 0;
		self.start.append(0);
		self.frontier.append(self.start);
		self.explored = [];
		self.end = self.maze.end;
		self.parent = {};
		self.path_cost = 0
		

	def next_nodes(self):
		state = min(self.frontier,key=lambda x:x[2]);
		self.frontier.remove(state);
		return state[0:2];

	def expand(self,state):
		new_state = list(state);
		new_state[0] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.explored.append(new_state[0:2]);
				self.parent[','.join(str(v) for v in new_state[0:2])] = state;
				self.cur_dist[','.join(str(v) for v in new_state[0:2])] = self.cur_dist[','.join(str(v) for v in state)]+1;
				A_heu = self._heuristic(new_state[0:2]) + self.cur_dist[','.join(str(v) for v in new_state[0:2])];
				new_state.append(A_heu);
				self.frontier.append(new_state);

		new_state = [];
		new_state = list(state);
		new_state[0] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.explored.append(new_state[0:2]);
				self.parent[','.join(str(v) for v in new_state[0:2])] = state;
				self.cur_dist[','.join(str(v) for v in new_state[0:2])] = self.cur_dist[','.join(str(v) for v in state)]+1;
				A_heu = self._heuristic(new_state[0:2]) + self.cur_dist[','.join(str(v) for v in new_state[0:2])];
				new_state.append(A_heu);
				self.frontier.append(new_state);

		new_state = [];
		new_state = list(state);
		new_state[1] -= 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.explored.append(new_state[0:2]);
				self.parent[','.join(str(v) for v in new_state[0:2])] = state;
				self.cur_dist[','.join(str(v) for v in new_state[0:2])] = self.cur_dist[','.join(str(v) for v in state)]+1;
				A_heu = self._heuristic(new_state[0:2]) + self.cur_dist[','.join(str(v) for v in new_state[0:2])];
				new_state.append(A_heu);
				self.frontier.append(new_state);

		new_state = [];
		new_state = list(state);
		new_state[1] += 1;
		if(self.maze.is_legal(new_state)):
			if new_state not in self.explored:
				self.explored.append(new_state[0:2]);
				self.parent[','.join(str(v) for v in new_state[0:2])] = state;
				self.cur_dist[','.join(str(v) for v in new_state[0:2])] = self.cur_dist[','.join(str(v) for v in state)]+1;
				A_heu = self._heuristic(new_state[0:2]) + self.cur_dist[','.join(str(v) for v in new_state[0:2])];
				new_state.append(A_heu);
				self.frontier.append(new_state);



""" The general search top level """
def general_search(maze,choice):
	""" Top-level search """
	if choice == '1':
		search = BFS_Search_Maze_Unique(maze);
	if choice == '2':
		search = DFS_Search_Maze_Unique(maze);
	if choice == '3':
		search = Greedy_Search_Maze_Unique(maze);
	if choice == '4':
		search = A_Search_Maze_Unique(maze);
	next_state = [];
	nodes_explored = 0
	while(search.is_empty()==False):
		next_state = search.next_nodes();
		nodes_explored += 1
		if(search.is_end(next_state)):
			break;
		search.expand(next_state);
	search.draw_path(next_state);
	search.display();
	print('Path Cost =',search.path_cost)
	print('Nodes Explored =',nodes_explored)

	
""" Read the maze """
if __name__ == "__main__":
	maze = [];
	indY = 0;
	indX = 0;
	with open(sys.argv[1]) as f_maze:
	    for line in f_maze:
	        maze.append([]);
	        indX = 0;
	        for char in line:
	        	if char != '\n':
		            maze[indY].append(char);
		            indX+=1;
	        indY+=1;
	new_maze = Maze_One_Dot(maze);
	new_maze.display();
	general_search(maze,sys.argv[2]);
