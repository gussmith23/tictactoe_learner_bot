from copy import deepcopy
from random import choice
from enum import Enum

class GameEvent(Enum):
	became_turn = 0
	won = 1
	lost = 2
	invalid_move = 3
	
class Game:
	UNCLAIMED = 3
	board = [[3 for i in range(3)] for j in range(3)]
	
	def __init__(self):
		"""
		
		"""
		self.board = deepcopy(self.board)
		self.turn = 0
		
	def make_move(self, location, player):
		"""
		False if no move made
		None if game is over
		True if move made
		"""
		if self.turn >= 9:
			return None
		if self.turn%2 != player:
			return False
		x = location[0]
		y = location[1]
		if self.board[y][x] != self.UNCLAIMED:
			return False
		self.board[y][x] = self.turn%2
		winner = find_winner(board = self.board, last_move = location)
		if winner is False:
			# progress the game.
			self.turn += 1
			return True
		else: 
			return winner
			
	def to_string(self):
		board = self.board
		return to_char(board[0][0]) + "|" + to_char(board[0][1]) + "|" + to_char(board[0][2]) + "\n"\
				+ "-+-+-\n"\
				+ to_char(board[1][0]) + "|" + to_char(board[1][1]) + "|" + to_char(board[1][2]) + "\n"\
				+ "-+-+-\n"\
				+ to_char(board[2][0]) + "|" + to_char(board[2][1]) + "|" + to_char(board[2][2]) + "\n"

def to_char(val_on_board):
	if val_on_board == 0:
		return "X"
	if val_on_board == 1:
		return "O"
	if val_on_board == 3:
		return " "
def find_winner(board, last_move):
	x = last_move[0]
	y = last_move[1]
	player = board[y][x]
	
	# check across the row
	row_win = True
	for col in range(3):
		if board[y][col] != player:
			row_win = False
			break
	
	if row_win:
		return player
		
	# check across the col
	col_win = True
	for row in range(3):
		if board[row][x] != player:
			col_win = False
			break
	
	if col_win:
		return player
		
	# check down the main diagonal (\)
	if x == y:
		main_diag_win = True
		for i in range(3):
			if board[i][i] != player:
				main_diag_win = False
				break
				
		if main_diag_win:
			return player
			
	# check down the cross diagonal (/)
	if x + y == len(board) - 1:
		cross_diag_win = True
		for i in range(3):
			if board[len(board)-1-i][i] != player:
				cross_diag_win = False
				break
				
		if cross_diag_win:
			return player
			
	return False

