"""
piece.py

Create piece class:
1. id in piece list
2. row in board
3. col in board
4. png for display
5. move generation function
"""

class Piece:
    # init a piece obj, should mostly stay the same except updates over time
    def __init__(self, id:int, r:int, c:int, color:bool, png, move_generator, evaluation_function):
        self.id = id
        self.r = r
        self.c = c
        self.color = color
        self.png = png
        self.move_generator = move_generator
        self.evaluation_function = evaluation_function
    
    def update_piece(self, new_png, new_generation):
        self.png = new_png
        self.mv_generation = new_generation
    
    def get_moves(self, board):
        return self.move_generator(self, board)

# TODO, add position and move additional vals
def white_king_evaluation(piece, board):
    return 2

# TODO, add position and move additional vals
def white_knight_evaluation(piece, board):
    return 4

# TODO, add position and move additional vals
def white_bishop_evaluation(piece, board):
    return 3

# TODO, add position and move additional vals
def white_rook_evaluation(piece, board):
    return 5

# TODO, add position and move additional vals
def white_pawn_evaluation(piece, board):
    return 1

# TODO, add position and move additional vals
def black_pawn_evaluation(piece, board):
    return -1
