#from board import *
#from board_extra_threebase import *
from board_extra_long import *
#from Algorithm import *
#from Algorithm_threeworker import *
from Algorithm_extra_long import *
import os
import sys
import time

#exmaple:  Y(OU) OF(FENSIVE) O(PPONENT) DE(FENSIVE) 1(game number)

if __name__ == "__main__":

#first player and its strategy
	if sys.argv[1] == 'Y':  #YOU
		PLAYER = 2;
	if sys.argv[1] == 'O':	#OPPONENT
		PLAYER = 1;
	if sys.argv[2] == 'OF': #OFFENSIVE
		STRATEGY = 1;
	if sys.argv[2] == 'DE': #DEFENSIVE
		STRATEGY = 2;

#second player and its strategy
	if sys.argv[3] == 'Y':
		PLAYER2 = 2;
	if sys.argv[3] == 'O':
		PLAYER2 = 1;
	if sys.argv[4] == 'OF':
		STRATEGY2 = 1;
	if sys.argv[4] == 'DE':
		STRATEGY2 = 2;


	Board = Board(OFFENSIVE,OFFENSIVE);
	Board.display()
	
	step = 0
	black_node_expand = 0
	white_node_expand = 0

	if (sys.argv[5]=='1'):
		while (1):
			mini_node = AB_Node(Board,PLAYER,STRATEGY);
			temp = Minimax_search(mini_node,MINI_DEPTH)
			action = temp[0];
			white_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;
			mini_node = AB_Node(Board,PLAYER2,STRATEGY2);
			temp = Minimax_search(mini_node,MINI_DEPTH);
			action = temp[0]
			black_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;

	if (sys.argv[5]=='2'):
		while (1):
			ab_node = AB_Node(Board,PLAYER,STRATEGY);
			temp = alpha_beta_search(ab_node,AB_DEPTH)
			action = temp[0];
			white_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;
			ab_node = AB_Node(Board,PLAYER2,STRATEGY2);
			temp = alpha_beta_search(ab_node,AB_DEPTH)
			action = temp[0];
			black_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;
	

	if (sys.argv[5]=='3'):
		while (1):
			mini_node = AB_Node(Board,PLAYER,STRATEGY);
			temp = Minimax_search(mini_node,MINI_DEPTH);
			action = temp[0]
			white_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;
			ab_node = AB_Node(Board,PLAYER2,STRATEGY2);
			temp = alpha_beta_search(ab_node,AB_DEPTH)
			action = temp[0];
			black_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;

	if (sys.argv[5]=='4'):
		while (1):
			ab_node = AB_Node(Board,PLAYER,STRATEGY);
			temp = alpha_beta_search(ab_node,AB_DEPTH)
			action = temp[0];
			white_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;
			mini_node = AB_Node(Board,PLAYER2,STRATEGY2);
			temp = Minimax_search(mini_node,MINI_DEPTH);
			action = temp[0]
			black_node_expand += temp[1]
			Board.change(action);
			step += 1
			Board.display();
			if(Board.end()):
				break;


	def get_captured(Board):
		cur_board = Board.board
		black_left = 0
		white_left = 0
		black_captured = 2*len(cur_board[0])
		white_captured = 2*len(cur_board[0])
		for y in range(len(cur_board)):
			for x in range(len(cur_board[0])):
				if cur_board[y][x] == 1:
					black_left+=1
				elif cur_board[y][x] == 2:
					white_left+=1
		black_captured -= black_left
		white_captured -= white_left
		return (black_captured,white_captured)


################ End ################
	Winner = Board.end()
	if Winner == 1:
		print('Winner: Black')
	elif Winner == 2:
		print('Winner: White')
	print('Total Moves = ',step)
	black_captured = get_captured(Board)[0]
	white_captured = get_captured(Board)[1]
	print('Black Captured ',white_captured,'White Pieces')
	print('White Captured ',white_captured,'Black Pieces')
	print('Nodes Expanded by Black: ',black_node_expand)
	print('Nodes Expanded by White: ',white_node_expand)
	

