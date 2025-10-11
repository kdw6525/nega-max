"""
piece.py

Create piece class:
1. id in piece list
2. row in board
3. col in board
4. png for display
5. move generation function
"""
import numpy as np
from typing import List, Tuple

class Piece:
    # init a piece obj, should mostly stay the same except updates over time
    def __init__(self, id:int, r:int, c:int, color:bool, png:str, move_generator, evaluation_function, zobrist_id:int):
        self.id = id
        self.r = r
        self.c = c
        self.color = color
        self.png = png
        self.move_generator = move_generator
        self.evaluation_function = evaluation_function
        self.zobrist_id = zobrist_id # index in the zb array that corresponds to random values 
    
    def update_piece(self, new_png, new_generation):
        self.png = new_png
        self.mv_generation = new_generation
    
    def evaluate(self, board, capture_data) -> int:
        return self.evaluation_function(self, board, capture_data)
    
    def get_moves(self, board, prev_move):
        return self.move_generator(self, board, prev_move)
    
    def is_captured(self):
        return self.c == -1
    
    def zb_hash(self, zb):
        return zb[self.zobrist_id][(self.r * 5) + self.c]
    
    def loc_zb_hash(self, zb, r, c):
        return zb[self.zobrist_id][(r * 5) + c]

    def __str__(self):
        return self.png

# TODO, add position and move additional vals
def white_king_evaluation(piece: Piece, board: List[List[Piece]], capture_data: np.typing.ArrayLike):
    piece_val = 2
    if piece.is_captured():
        return 0 
    eval = piece_val
    if capture_data[1]:
        eval -= piece_val
    else:
        eval += capture_data[0]
    return eval

# TODO, add position and move additional vals
def white_knight_evaluation(piece: Piece, board: List[List[Piece]], capture_data: np.typing.ArrayLike):
    piece_val = 4
    if piece.is_captured():
        return 0 
    eval = piece_val
    if capture_data[1]:
        eval -= piece_val
    else:
        eval += capture_data[0]
    return eval

# TODO, add position and move additional vals
def white_bishop_evaluation(piece: Piece, board: List[List[Piece]], capture_data: np.typing.ArrayLike):
    piece_val = 3
    if piece.is_captured():
        return 0 
    eval = piece_val
    if capture_data[1]:
        eval -= piece_val
    else:
        eval += capture_data[0]
    return eval

# TODO, add position and move additional vals
def white_rook_evaluation(piece: Piece, board: List[List[Piece]], capture_data: np.typing.ArrayLike):
    piece_val = 5
    if piece.is_captured():
        return 0 
    eval = piece_val
    if capture_data[1]:
        eval -= piece_val
    else:
        eval += capture_data[0]
    return eval

# TODO, add position and move additional vals
def white_pawn_evaluation(piece: Piece, board: List[List[Piece]], capture_data: np.typing.ArrayLike):
    piece_val = 1
    if piece.is_captured():
        return 0 
    eval = piece_val
    if capture_data[1]:
        eval -= piece_val
    else:
        eval += capture_data[0]
    return eval

# TODO, add position and move additional vals
def black_pawn_evaluation(piece: Piece, board: List[List[Piece]], capture_data: np.typing.ArrayLike):
    piece_val = 1
    if piece.is_captured():
        return 0 
    eval = piece_val
    
    if capture_data[1]:
        eval -= piece_val
    else:
        eval += capture_data[0]
    return eval * -1 # negate because black player
