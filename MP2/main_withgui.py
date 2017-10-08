from board import *
from Algorithm import *
from gui import *
#from Algorithm import *
import os
import sys


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
	root = tk.Tk()
	board = GameBoard(root)
	board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
	player1 = tk.PhotoImage(file ="white_pawn.gif")
	player2 = tk.PhotoImage(file ="black_pawn.gif")
	name = 'A'

	while (1):
		ab_node = AB_Node(Board,PLAYER,STRATEGY);
		action = alpha_beta_search(ab_node,AB_DEPTH);
		Board.change(action);
		Board.display();

		for row in range(0,8):
			for col in range(0,8):
				if (Board.board[row][col] == 1):
					board.addpiece(name[0]+str(row)+str(col), player2, row,col)

				if (Board.board[row][col] == 2):
					board.addpiece(name[0]+str(row)+str(col), player1, row,col)

		root.update_idletasks()
		root.update()
		tm.sleep(1)
		board.deleteAllPiece()
		if(Board.end()):
			break;
	
		ab_node = AB_Node(Board,PLAYER2,STRATEGY2);
		action = alpha_beta_search(ab_node,AB_DEPTH);
		Board.change(action);
		Board.display();

		for row in range(0,8):
			for col in range(0,8):
				if (Board.board[row][col] == 1):
					board.addpiece(name[0]+str(row)+str(col), player2, row,col)

				if (Board.board[row][col] == 2):
					board.addpiece(name[0]+str(row)+str(col), player1, row,col)

		root.update_idletasks()
		root.update()
		tm.sleep(1)
		board.deleteAllPiece()












