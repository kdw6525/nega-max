"""
board.py
Handles all board related functions and initializations
"""
from piece import Piece, black_pawn_evaluation, white_pawn_evaluation, white_knight_evaluation, white_bishop_evaluation, white_king_evaluation, white_rook_evaluation
from moves import Move, black_pawn_moves, white_pawn_moves, white_knight_moves, white_bishop_moves, white_king_moves, white_rook_moves
import random

# Board initialization, populated when main is ran
BOARD_SIZE = 480
ROWS, COLS = 8, 5

board = [
    [None] * 5,
    [None] * 5,
    [None] * 5,
    [None] * 5,
    [None] * 5,
    [None] * 5,
    [None] * 5,
    [None] * 5,
]

piece_lst = [None] * 24 # black pieces are 0-14, white pieces are 15-23

# Make the initial board state, if not given a back rank for white it will randomize
# white_back_rank format, must contain all 4 pieces: " knbr", or "r bnk", ect...
def fill_board(white_back_rank=None):
    
    # initiate black pieces
    i = 0
    for r in range(3):
        for c in range(COLS):
            piece = Piece(id=i, r=r, c=c, color=False, png='bp', 
                          move_generator=black_pawn_moves, 
                          evaluation_function=black_pawn_evaluation)
            piece_lst[i] = piece
            board[r][c] = piece
            i +=1
            
    # initiate white pawns on 7th rank (r = 6)
    for c in range(COLS):
        piece = Piece(id=i, r=6, c=c, color=True, png='wp', 
                      move_generator=white_pawn_moves, 
                      evaluation_function=white_pawn_evaluation)
        piece_lst[i] = piece
        board[6][c] = piece
        i += 1

    # make the back rank
    # initalize the pieces
    king = Piece(id=i, r=7, c=0, color=True, png='wk', 
                 move_generator=white_king_moves, 
                 evaluation_function=white_king_evaluation)
    piece_lst[i] = king

    knight = Piece(id=i+1, r=7, c=0, color=True, png='wn', 
                   move_generator=white_knight_moves, 
                   evaluation_function=white_knight_evaluation)
    piece_lst[i+1] = knight

    bishop = Piece(id=i+2, r=7, c=0, color=True, png='wb', 
                   move_generator=white_bishop_moves, 
                   evaluation_function=white_bishop_evaluation)
    piece_lst[i+2] = bishop

    rook = Piece(id=i+3, r=7, c=0, color=True, png='wr', 
                 move_generator=white_rook_moves, 
                 evaluation_function=white_rook_evaluation)
    piece_lst[i+3] = rook

    if white_back_rank is None:
        char_list = list('knrb ')
        random.shuffle(char_list)
        white_back_rank = "".join(char_list)
    
    c = 0
    for char in white_back_rank:
        if char == " ":
            c += 1
            continue
        if char == "k":
            king.c = c
            board[7][c] = king
            c+=1
            continue
        if char == "n":
            knight.c = c
            board[7][c] = knight
            c+=1
            continue
        if char == "b":
            bishop.c = c
            board[7][c] = bishop
            c+=1
            continue
        if char == "r":
            rook.c = c
            board[7][c] = rook
            c+=1
            continue

    return

def make_board_move(mv: Move):
    # mv_piece = board[selected[0]][selected[1]]
    # mv_piece.r, mv_piece.c = row, col
    # board[row][col] = mv_piece
    # board[selected[0]][selected[1]] = None
    # selected = rs, cs
    
    mv.piece.r, mv.piece.c = mv.re, mv.ce
    board[mv.re][mv.ce] = mv.piece
    board[mv.rs][mv.cs] = None

    if mv.capture:
        if mv.enpassant_cap:
            board[mv.piece.r-1][mv.piece.c] = None
        mv.capture.r, mv.capture.c = -1, -1
    
    if mv.promotion:
        mv.piece.png = 'wr'
        mv.piece.move_generator = white_rook_moves
        mv.piece.evaluation_function = white_rook_evaluation

    return

def undo_board_move(mv: Move):
    # reset positions! and piece data
    mv.piece.r, mv.piece.c = mv.rs, mv.cs
    board[mv.rs][mv.cs] = mv.piece
    board[mv.re][mv.ce] = None

    # restore captured piece
    if mv.capture:
        if mv.enpassant_cap:
            mv.capture.r, mv.capture.c = mv.rs, mv.ce
            board[mv.rs][mv.ce] = mv.capture
        else:
            mv.capture.r, mv.capture.c = mv.re, mv.ce
            board[mv.re][mv.ce] = mv.capture
    
    # restore promotion
    if mv.promotion:
        mv.piece.png = 'wp'
        mv.piece.move_generator = white_pawn_moves
        mv.piece.evaluation_function = white_pawn_evaluation