import os
import sys
from copy import deepcopy


EMPTY = 0
BLACK = 1
WHITE = 2
OFFENSIVE = 1
DEFENSIVE = 2
LEFT = 1
STRIGHT = 2
RIGHT = 3


class Board:
	def __init__(self,Black_Playstyle,White_Playstyle):
		self.board = []
		self._start()
		self.white = self.find_white()
		self.black = self.find_black()  
		self.height = len(self.board)
		self.width = len(self.board[0])
		self.playstyle = [Black_Playstyle, White_Playstyle]    #1: Offensive #2: Defensive


	def _start(self):
		for y in range(0,8):
			temp_board = []
			for x in range(0,8):
				if (y==0) or (y==1):
					temp_board.append(BLACK)    # Black = 1
				elif (y==6) or (y==7):
					temp_board.append(WHITE)    # White = 2
				else:
					temp_board.append(EMPTY)    # Empty = 0
			self.board.append(temp_board)


	def find_white(self):
		white_piece = []
		for row in self.board:
			for position in row:
				if position == WHITE:
					white_piece.append(position)
		return white_piece


	def find_black(self):
		black_piece = []
		for row in self.board:
			for position in row:
				if position == 1:
					black_piece.append(position)
		return black_piece


	def next_move(self,Board,Player,Piece,Move):
		new_board = deepcopy(self.board)        
		if Player==BLACK:                                      # Black, Moving Downwards
			if Move==LEFT:                                     # Left-Diagonal
				self.board[Piece[0]+1][Piece[1]+1][2] = BLACK  
				self.board[Piece[0]][Piece[1]][2] = 0
			elif Move==STRIGHT:                                # Straight Forward
				self.board[Piece[0]+1][Piece[1]][2] = BLACK
				self.board[Piece[0]][Piece[1]][2] = 0
			elif Move==RIGHT:                                  # Right-Diagonal
				self.board[Piece[0]+1][Piece[1]-1][2] = BLACK
				self.board[Piece[0]][Piece[1]][2] = 0
		elif Player==WHITE:                                    # White, Moving Upwards
			if Move==LEFT:                                     # Left-Diagonal
				self.board[Piece[0]-1][Piece[1]-1][2] = WHITE  
				self.board[Piece[0]][Piece[1]][2] = 0
			elif Move==STRAIGHT:                               # Straight Forward
				self.board[Piece[0]-1][Piece[1]][2] = WHITE
				self.board[Piece[0]][Piece[1]][2] = 0
			elif Move==RIGHT:                                  # Right-Diagonal
				self.board[Piece[0]-1][Piece[1]+1][2] = WHITE
				self.board[Piece[0]][Piece[1]][2] = 0
		return new_board


	def next_move_valid(self,board,player,piece,move):
		if self._range_valid(board,player,piece,move)==False:       
			return False
		if self._target_position_valid(board,player,piece,move)==False:
			return False
		if move==STRAIGHT:
			if player==BLACK:
				if board[piece[0]+1][piece[1]][2]==WHITE:
					return False
			elif player==WHITE:
				if board[piece[0]-1][piece[1]][2]==BLACK:
					return False


	def _range_valid(self,board,player,piece,move):
		if (piece[0]!=0) and (piece[0]!=7) and (piece[1]!=0) and (piece[1]!=7):
			return True         # Piece Not on Edge
		else:   
			if piece[0]==0:         # Top Row
				if (player==WHITE) and (move==STRAIGHT):
					return False
			if piece[0]==7:         # Bottom Row
				if (player==BLACK) and (move==STRAIGHT):
					return False
			if piece[1]==0:         # Left Column
				if (player==BLACK) and (move==RIGHT):
					return False
				elif (player==WHITE) and (move==LEFT):
					return False
			if piece[1]==7:         # Rigth Column
				if (player==BLACK) and (move==LEFT):
					return False
				elif (player==WHITE) and (move==RIGHT):
					return False
			return True


	def _target_position_valid(self,board,player,piece,move):      # Check if Target Position Has Same Color
		if player==BLACK:
			if move==LEFT:
				if board[piece[0]][piece[1]+1][2]==BLACK:
					return False
			elif move==STRAIGHT:
				if board[piece[0]+1][piece[1]][2]==BLACK:
					return False
			elif move==RIGHT:
				if board[piece[0]][piece[1]-1][2]==BLACK:
					return False

		elif player==WHITE:
			if move==LEFT:
				if board[piece[0]][piece[1]-1][2]==WHITE:
					return False
			elif move==STRAIGHT:
				if board[piece[0]-1][piece[1]][2]==WHITE:
					return False
			elif move==RIGHT:
				if board[piece[0]][piece[1]+1][2]==WHITE:
					return False


	def display(self):
		print('Note: Black=1; White=2; Empty=0')
		for row in self.board:
			string=""
			for position in row:
				string+=str(position)
					#print(position)
			print(string)

	def change(self,action):
		print('action = ',action)
		self.board[action[2]][action[3]] = self.board[action[0]][action[1]]
		self.board[action[0]][action[1]] = 0
	 
	def end(self):
		#print('end')
		flag_black = 0   # check if there are black pieces left, 1 if yes
		flag_white = 0   # check if there are black pieces left, 1 if yes
		Winner = 0
		for y in range(len(self.board)):
			for x in range(len(self.board[0])):
				if (y==0):
					if self.board[y][x]==WHITE:   # white piece reaches black home base (top row)
						Winner = WHITE
					if self.board[y][x]==BLACK:   # there are black pieces left
						flag_black = 1
				#elif (y==len(self.board)-1):
				elif y == 7:
					if self.board[y][x]==BLACK:   # black piece reaches white home base (bottom row)
						Winner = BLACK
					if self.board[y][x]==WHITE:   # there are white pieces left
						flag_white = 1
				else:                    # row 1-6
					if self.board[y][x]==BLACK:   # there are black pieces left
						flag_black = 1
					if self.board[y][x]==WHITE:   # there are white pieces left
						flag_white = 1

		if flag_black==0:    # there are no black pieces left
			Winner = WHITE         # White wins
		elif flag_white==0:    # there are no white pieces left
			Winner = BLACK         # Black wins

		if Winner!=0:
			return Winner
		else:
			return False




























