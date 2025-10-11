"""
board.py
Handles all board related functions and initializations
"""
from piece import Piece, black_pawn_evaluation, white_pawn_evaluation, white_knight_evaluation, white_bishop_evaluation, white_king_evaluation, white_rook_evaluation
from moves import Move, black_pawn_moves, white_pawn_moves, white_knight_moves, white_bishop_moves, white_king_moves, white_rook_moves
import random
from typing import List, Tuple
import numpy as np

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

w_captured = 0
b_captured = 0

# Make the initial board state, if not given a back rank for white it will randomize
# white_back_rank format, must contain all 4 pieces: " knbr", or "r bnk", ect...
def fill_board(white_back_rank=None):
    # initiate black pieces
    i = 0
    for r in range(3):
        for c in range(COLS):
            piece = Piece(id=i, r=r, c=c, color=False, png='bp', 
                          move_generator=black_pawn_moves, 
                          evaluation_function=black_pawn_evaluation,
                          zobrist_id=0)
            piece_lst[i] = piece
            board[r][c] = piece
            i +=1
            
    # initiate white pawns on 7th rank (r = 6)
    for c in range(COLS):
        piece = Piece(id=i, r=6, c=c, color=True, png='wp', 
                      move_generator=white_pawn_moves, 
                      evaluation_function=white_pawn_evaluation,
                      zobrist_id=1)
        piece_lst[i] = piece
        board[6][c] = piece
        i += 1

    # make the back rank
    # initalize the pieces
    king = Piece(id=i, r=7, c=0, color=True, png='wk', 
                 move_generator=white_king_moves, 
                 evaluation_function=white_king_evaluation,
                 zobrist_id=2)
    piece_lst[i] = king

    knight = Piece(id=i+1, r=7, c=0, color=True, png='wn', 
                   move_generator=white_knight_moves, 
                   evaluation_function=white_knight_evaluation,
                   zobrist_id=3)
    piece_lst[i+1] = knight

    bishop = Piece(id=i+2, r=7, c=0, color=True, png='wb', 
                   move_generator=white_bishop_moves, 
                   evaluation_function=white_bishop_evaluation,
                   zobrist_id=4)
    piece_lst[i+2] = bishop

    rook = Piece(id=i+3, r=7, c=0, color=True, png='wr', 
                 move_generator=white_rook_moves, 
                 evaluation_function=white_rook_evaluation,
                 zobrist_id=5)
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

def make_board_move(mv: Move, zb=None, board_zb_hash=None):
    # mv_piece = board[selected[0]][selected[1]]
    # mv_piece.r, mv_piece.c = row, col
    # board[row][col] = mv_piece
    # board[selected[0]][selected[1]] = None
    # selected = rs, cs
    global b_captured
    global w_captured

    mv.piece.r, mv.piece.c = mv.re, mv.ce
    board[mv.re][mv.ce] = mv.piece
    board[mv.rs][mv.cs] = None

    if mv.capture:
        if mv.enpassant_cap:
            board[mv.piece.r-1][mv.piece.c] = None
        mv.capture.r, mv.capture.c = -1, -1
        if mv.capture.color: # if white we increment
            w_captured = w_captured + 1
        else:
            b_captured = b_captured + 1
    
    # promote the piece, changing important piece data:
    match mv.promotion:
        case 1:
            mv.piece.png = 'wr'
            mv.piece.move_generator = white_rook_moves
            mv.piece.evaluation_function = white_rook_evaluation
            mv.piece.zobrist_id = 5
        case 2:
            mv.piece.png = 'wn'
            mv.piece.move_generator = white_knight_moves
            mv.piece.evaluation_function = white_knight_evaluation
            mv.piece.zobrist_id = 3
        case 3:
            mv.piece.png = 'wk'
            mv.piece.move_generator = white_king_moves
            mv.piece.evaluation_function = white_king_evaluation
            mv.piece.zobrist_id = 2
        case 4:
            mv.piece.png = 'wb'
            mv.piece.move_generator = white_bishop_moves
            mv.piece.evaluation_function = white_bishop_evaluation
            mv.piece.zobrist_id = 4

    # calc new hash now since after promotion to keep promotion data
    if zb is not None:
        board_zb_hash = update_board_zb_hash(zb=zb, board_zb_hash=board_zb_hash, mv=mv)
        # print(board_zb_hash)
    return board_zb_hash

def undo_board_move(mv: Move, zb=None, board_zb_hash=None):
    # reset positions! and piece data
    global b_captured
    global w_captured

    # calc new hash now since before promotion and before promotion data is lost
    if zb is not None:
        board_zb_hash = update_board_zb_hash(zb=zb, board_zb_hash=board_zb_hash, mv=mv)
        # print(board_zb_hash)
    
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

        if mv.capture.color: # if white we decrement
            w_captured = w_captured - 1
        else:
            b_captured = b_captured - 1
    
    # restore promotion
    if mv.promotion:
        mv.piece.png = 'wp'
        mv.piece.move_generator = white_pawn_moves
        mv.piece.evaluation_function = white_pawn_evaluation
        mv.piece.zobrist_id = 1

    return board_zb_hash
    
def evaluate_board(prev_move: Move) -> int:
    # iterate through pieces and evaluate each
    # the more in depth the evaluation, the better chance of pruning (probably)
    eval = 0

    # generate moves, make list for each piece [# of captures I can make, # of moves to capture me]
    # if I am ever captured, I have to evaluate how meaning full that is for the game
    # if I can capture, it doesn't matter if I'm going to get captured now
    mvs = get_all_moves(prev_move=prev_move)
    pc_cap_mvs = np.zeros(shape=(24, 2), dtype=int) # [# of captures I can make, # of moves to capture me]
    for cap_mv in mvs[0]:
        if cap_mv.capture:
            pc_cap_mvs[cap_mv.piece.id][0] = pc_cap_mvs[cap_mv.piece.id][0] + 1
            pc_cap_mvs[cap_mv.capture.id][1] = pc_cap_mvs[cap_mv.capture.id][1] + 1


    # evaluation also checks 
    for pc in piece_lst:
        eval += pc.evaluate(board, pc_cap_mvs[pc.id])
    
    return eval

def check_win() -> int:
    # check if black piece on back rank
    # check if all white pieces are captured
    # check if all black pieces are captured
    
    # captures first
    if b_captured == 15:
        return 1000
    if w_captured == 9:
        return -1000
    
    for pc in board[7]: # for each pc in back rank check if black
        if pc and not pc.color:
            return -1000
    
    return 0

def get_player_moves(turn:bool, prev_move: Move) -> Tuple[List[Move], List[Move]]:
    # init lists
    captures = []
    moves = []

    # depending on the player turn, get the moves for active player's piece
    if turn:
        for pc in piece_lst[15:24]:
            if not pc.is_captured():
                mvs = pc.get_moves(board, prev_move) # (captures, moves)
                captures += mvs[0]
                moves += mvs[1]
    else:
        for pc in piece_lst[0:15]:
            if not pc.is_captured():
                mvs = pc.get_moves(board, prev_move) # (captures, moves)
                captures += mvs[0]
                moves += mvs[1]

    return (captures, moves)

def get_all_moves(prev_move: Move) -> Tuple[List[Move], List[Move]]:
    # init lists
    captures = []
    moves = []

    # for every piece we have calc its moves!
    for pc in piece_lst:
        if not pc.is_captured():
            mvs = pc.get_moves(board, prev_move) # (captures, moves)
            captures += mvs[0]
            moves += mvs[1]

    return (captures, moves)

def print_board():
    # loop through board and print piece or spaces 
    board_str = "  "
    for row in board:
        for pc in row:
            if pc:
                board_str += f'{pc} '
            else:
                board_str += '   '
        board_str += '\n'
    print(board_str)

def calculate_zb_hash(zb:np.typing.ArrayLike):
    # get the full board hash
    zh_hash = piece_lst[0].zb_hash(zb)
    for pc in piece_lst[1:]:
        zh_hash = zh_hash ^ pc.zb_hash(zb) # XOR
    return zh_hash

def update_board_zb_hash(board_zb_hash, zb:np.typing.ArrayLike, mv: Move):
    # update the hash
    # new = old ^ old_pos ^ new_pos (^ captured_pos)

    # prints to verify hash works!
    # print()
    # print(board_zb_hash)

    if mv.promotion:
        board_zb_hash = board_zb_hash ^ zb[1][(mv.rs * 5) + mv.cs] # starting condition was a pawn!
    else:
        board_zb_hash = board_zb_hash ^ mv.piece.loc_zb_hash(zb=zb, r=mv.rs, c=mv.cs)

    # print(board_zb_hash)
    board_zb_hash = board_zb_hash ^ mv.piece.loc_zb_hash(zb=zb, r=mv.re, c=mv.ce)

    # print(board_zb_hash)
    if mv.capture:
        board_zb_hash = board_zb_hash ^ mv.capture.loc_zb_hash(zb=zb, r=mv.capture.r, c=mv.capture.c)
        # print(board_zb_hash)
    return board_zb_hash
