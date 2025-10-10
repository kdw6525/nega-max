# two search methods, nega_max

# Implementation from lecture
#
# 1. Heuristic values are from the perspective of the acting player
# 2. Alpha a lower bound on the best value that the acting player can achieve
# 3. Beta is an upper bound on what the opponent can achieve
#

from board import evaluate_board, check_win, get_player_moves, make_board_move, undo_board_move, print_board
from moves import Move

def nega_max_root(prev_move: Move, d:int, alpha: int, beta:int, turn:bool) -> Move:
    # root iteration set up val_flip
    # return move with best score
    win = check_win()
    if win:
        return None
    if d == 0:
        return None
    
    # get moves and check stalemate
    mvs = get_player_moves(turn=turn, prev_move=prev_move)
    if not mvs[0] and not mvs[1]: # if both are empty aka stalemate
        return None
    
    val_flip = 1 if turn else -1
    score = -1001
    mv = None
    for cap_mv in mvs[0]:
        make_board_move(mv=cap_mv)
        val = -1 * nega_max(prev_move=cap_mv, d=d-1, alpha=-1*beta, beta=-1*alpha, val_flip=val_flip*-1, turn=not turn)
        print(val)
        if val > score:
            score = val
            mv = cap_mv
            if score > alpha:
                alpha = score
            if score >= beta:
                print_board()
                print('PRUNE')
                undo_board_move(mv=cap_mv)
                return mv
        undo_board_move(mv=cap_mv)
    for movement_mv in mvs[1]:
        # do the thing again
        make_board_move(mv=movement_mv)
        val = -1 * nega_max(prev_move=movement_mv, d=d-1, alpha=-1*beta, beta=-1*alpha, val_flip=val_flip*-1, turn=not turn)
        if val > score:
            score = val
            mv = movement_mv
            if score > alpha:
                alpha = score
            if score >= beta:
                print_board()
                print('PRUNE')
                undo_board_move(mv=movement_mv)
                return mv
        undo_board_move(mv=movement_mv)

    return mv

def nega_max(prev_move:Move, d: int, alpha: int, beta:int, turn:bool, val_flip:int) -> int:
    # check if draw by getting moves, but check depth/win before anything
    win = check_win()
    if win:
        print_board()
        return win * val_flip
    if d == 0:
        print_board()
        return evaluate_board() * val_flip
    # get moves and check for stalemate
    mvs = get_player_moves(turn=turn, prev_move=prev_move)
    if not mvs[0] and not mvs[1]: # if both are empty aka stalemate
        return 0
    
    score = -1000
    for cap_mv in mvs[0]:
        # do the thing
        make_board_move(mv=cap_mv)
        val = -1 * nega_max(prev_move=cap_mv, d=d-1, alpha=-1*beta, beta=-1*alpha, val_flip=val_flip*-1, turn=not turn)
        if val > score:
            score = val
            if score > alpha:
                alpha = score
            if score >= beta:
                print_board()
                print('PRUNE')
                undo_board_move(mv=cap_mv)
                return score * val_flip
        undo_board_move(mv=cap_mv)

    for movement_mv in mvs[1]:
        # do the thing again
        make_board_move(mv=movement_mv)
        val = -1 * nega_max(prev_move=movement_mv, d=d-1, alpha=-1*beta, beta=-1*alpha, val_flip=val_flip*-1, turn=not turn)
        if val > score:
            print(val)
            score = val
            if score > alpha:
                alpha = score
            if score >= beta:
                print_board()
                print('PRUNE')
                undo_board_move(mv=movement_mv)
                return score * val_flip
        undo_board_move(mv=movement_mv)

    return score * val_flip