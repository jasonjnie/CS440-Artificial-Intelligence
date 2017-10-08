import os
import sys
#from board_extra_threebase import *
from board import *
from copy import deepcopy;

YOU = 2;
OPPONENT = 1;
OFF_WEIGHT = [0.8,0.2]
DEF_WEIGHT = [0.2,0.8]
EAT_WEIGHT = 1
AB_DEPTH = 5 # 5 for basic implementation & 5*10 board bonus, 5 for threebase bonus
MINI_DEPTH = 3
OFFENSIVE = 1
DENFENSIVE = 2
node = 0;


class AB_Node:
	def __init__(self,Board,player,strategy):
		self.Board = Board;
		self.player = player;
		self.oringal = player;
		self.strategy = strategy;
		self.node_expand = 0

	def is_end(self):
		return self.Board.end();

	""" All the function to get the next action """
	# return [[y,x,y',x'],...]
	def get_action(self):
		# Find the next player
		action = [];
		board = self.Board.board
		if self.player == YOU:
			next_player = OPPONENT
		if self.player == OPPONENT:
			next_player = YOU
		player = self.player

		if player == YOU:
			for y in range(self.Board.height):
				for x in range(self.Board.width):
					if board[y][x] == player:
						if y == 0:
							continue;
						if x == 0:
							if board[y-1][x+1] != player:
								action.append([y,x,y-1,x+1])
							if board[y-1][x] != player:
								if board[y-1][x] != next_player:
									action.append([y,x,y-1,x])
							continue;
						if x == self.Board.width-1:
							if board[y-1][x-1] != player:
								action.append([y,x,y-1,x-1])
							if board[y-1][x] != player:
								if board[y-1][x] != next_player:
									action.append([y,x,y-1,x])
							continue;
						else:
							if board[y-1][x+1] != player:
								action.append([y,x,y-1,x+1])
							if board[y-1][x-1] != player:
								action.append([y,x,y-1,x-1])
							if board[y-1][x] != player:
								if board[y-1][x] != next_player:
									action.append([y,x,y-1,x])

		if player == OPPONENT:
			for y in range(self.Board.height-1,-1,-1):
				for x in range(self.Board.width-1,-1,-1):
					if board[y][x] == player:
						if y == self.Board.height - 1:
							continue;
						if x == self.Board.width-1:
							if board[y+1][x-1] != player:
								action.append([y,x,y+1,x-1])
							if board[y+1][x] != player:
								if board[y+1][x] != next_player:
									action.append([y,x,y+1,x])
							continue;
						if x == 0:
							if board[y+1][x+1] != player:
								action.append([y,x,y+1,x+1])
							if board[y+1][x] != player:
								if board[y+1][x] != next_player:
									action.append([y,x,y+1,x])
							continue;
						else:
							if board[y+1][x-1] != player:
								action.append([y,x,y+1,x-1])
							if board[y+1][x+1] != player:
								action.append([y,x,y+1,x+1])
							if board[y+1][x] != player:
								if board[y+1][x] != next_player:
									action.append([y,x,y+1,x])
		return action;

	def succ(self,action):
		new_board = deepcopy(self.Board);
		player = self.player;

		new_board.board[action[2]][action[3]] = new_board.board[action[0]][action[1]];
		new_board.board[action[0]][action[1]] = 0;

		if player == YOU:
			next_player = OPPONENT
		if player == OPPONENT:
			next_player = YOU

		next_node = AB_Node(new_board,next_player,self.strategy);
		next_node.oringal = self.oringal;
		return next_node

	""" All the heuristic """
	def heu(self):
		if self.strategy == OFFENSIVE:
			return self.off_heu(self.oringal)
		else:
			return self.def_heu(self.oringal)

	def off_heu(self,player):
		if player == YOU:
			return OFF_WEIGHT[0]*self.eval_fun(YOU) - OFF_WEIGHT[1]*self.eval_fun(OPPONENT)
		else:
			return OFF_WEIGHT[0]*self.eval_fun(OPPONENT) - OFF_WEIGHT[1]*self.eval_fun(YOU)


	def def_heu(self,player):
		if player == YOU:
			return DEF_WEIGHT[0]*self.eval_fun(YOU) - DEF_WEIGHT[1]*self.eval_fun(OPPONENT)
		else:
			return DEF_WEIGHT[0]*self.eval_fun(OPPONENT) - DEF_WEIGHT[1]*self.eval_fun(YOU)

	def any_prey(self,y,x,player):
		board = self.Board.board;
		if player == YOU:
			if y == 0:
				return 0;
			if x == 0:
				if board[y-1][x+1] == OPPONENT:
					return EAT_WEIGHT*(y)*(y);
				else:
					return 0;
			if x == self.Board.width-1:
				if board[y-1][x-1] == OPPONENT:
					return EAT_WEIGHT;
				else:
					return 0;
			if board[y-1][x+1] == OPPONENT or board[y-1][x-1]== OPPONENT:
				return EAT_WEIGHT;

		if player == OPPONENT:
			if y == self.Board.height - 1:
				return 0;
			if x == 0:
				if board[y+1][x+1] == YOU:
					return EAT_WEIGHT;
				else:
					return 0;
			if x == self.Board.width-1:
				if board[y+1][x-1] == YOU:
					return EAT_WEIGHT;
				else:
					return 0;
			if board[y+1][x+1] == YOU or board[y+1][x-1] == YOU:
				return EAT_WEIGHT;
		return 0;

	def eval_fun(self,player):
		board = self.Board.board;
		score = 0;
		for y in range(self.Board.height):
			for x in range(self.Board.width):
				if board[y][x] == player:
					if player == YOU:
						score += (len(board)-y)*(len(board)-y);
					if player == OPPONENT:
						score += (y+1)*(y+1)
		return score;

	def display(self):
		self.Board.display();

def alpha_beta_search(ab_node,depth):
	global node
	node = 0
	retVal = Max_value(ab_node,float('-inf'),float('inf'),depth-1)
	return (retVal[1],retVal[2])

def Max_value(ab_node,a,b,depth):
	global node
	winner = ab_node.is_end()
	if winner:
		if winner == ab_node.oringal:
			return float('inf');
		else:
			return float('-inf')
	if depth == 0:
		return ab_node.heu();
	v = float('-inf');
	actions = ab_node.get_action();
	retAction = [];
	for action in actions:
		node += 1
		score = Min_value(ab_node.succ(action),a,b,depth-1)

		if v < score:
			v = score;
			retAction = action;
		if v >= b:
			if depth == AB_DEPTH-1:
				return (v,action,node); 
			else:
				return v;
		a = max(a,v);
	if depth == AB_DEPTH-1:
		if len(retAction) != 0:
			return (v,retAction,node);
		else:
			return (v,actions[0],node);
	else:
		return v;

def Min_value(ab_node,a,b,depth):
	global node
	winner = ab_node.is_end()
	if winner:
		if winner == ab_node.oringal:
			return float('inf');
		else:
			return float('-inf')
	if depth == 0:
		return ab_node.heu();
	v = float('inf');
	actions = ab_node.get_action();
	for action in actions:
		node += 1
		score = Max_value(ab_node.succ(action),a,b,depth-1)
		v = min(v,score)
		if v <= a:
			return v;
		b = min(b,v);
	return v;


def Minimax_search(ab_node,depth):
	global node
	if depth == MINI_DEPTH:
		node = 0
	winner = ab_node.is_end()
	if winner:
		if winner == ab_node.oringal:
			return float('inf');
		else:
			return float('-inf')
	if depth == 0:
		return ab_node.heu();

	
	actions = ab_node.get_action();
	retAction = actions[0];
	if ab_node.player == ab_node.oringal:
		v = float('-inf');
		for action in actions:
			node += 1
			
			score = Minimax_search(ab_node.succ(action),depth-1)
			if v < score:
				v = score;
				retAction = action;
	else:
		v = float('inf');
		for action in actions:
			node += 1

			score = Minimax_search(ab_node.succ(action),depth-1);
			if v > score:
				v = score;
				retAction = action;

	if depth == MINI_DEPTH:
		return (retAction,node)
	else:
		return v;
"""
Board = Board(OFFENSIVE,DEFENSIVE);
node = AB_Node(Board,OPPONENT,OFFENSIVE);
node.display()
action = Minimax_search(node,MINI_DEPTH);
Board.change(action);
node.display()
"""

