"""
moves.py

create move generation functions for:
1. white pawn
2. white king
3. white knight
4. white bishop
5. white rook
6. black pawn

Create move class:
1. id of piece to move
2. start row
3. start col
4. end row
5. end col
6. id of piece captured, else None
7. promotion bool
"""

from piece import Piece
from typing import List, Tuple

ROWS, COLS = 8, 5

class Move:
    # track the piece, start, destination, captured piece, and if promotion
    def __init__(self, piece: Piece, rs:int, cs:int, re:int, ce:int, capture: Piece, promotion: bool, enpassant:bool, enpassant_cap:bool):
        self.piece = piece
        self.rs = rs
        self.cs = cs
        self.re = re
        self.ce = ce
        self.capture = capture
        self.promotion = promotion
        self.enpassant = enpassant
        self.enpassant_cap = enpassant_cap
    
    def __str__(self):
        if self.capture:
            return f"{self.piece} ({self.rs+1}, {self.cs+1}) to ({self.re+1}, {self.ce+1}) [capture: {self.capture} ({self.capture.r+1}, {self.capture.c+1})]"
        else:
            return f"{self.piece} ({self.rs+1}, {self.cs+1}) to ({self.re+1}, {self.ce+1})"


# Move generation functions
def white_king_moves(piece:Piece, board: List[List[Piece]], prev_mv: Move) -> Tuple[List[Move], List[Move]]:
    moves = []
    captures = []

    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == dc:
                continue

            nr = piece.r + dr
            nc = piece.c + dc

            if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                continue

            cap = board[nr][nc]
            if cap:
                if cap.color != piece.color:
                    captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=cap, promotion=False, enpassant=False, enpassant_cap=False))
            else:
                moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=None, promotion=False, enpassant=False, enpassant_cap=False))


    return (captures, moves)

def white_knight_moves(piece:Piece, board: List[List[Piece]], prev_mv: Move) -> Tuple[List[Move], List[Move]]:
    moves = []
    captures = []

    # can move in jumping L directions
    d = [
            (2, 1),     (1, 2), 
            (-2, 1),   (-1, 2),
            (2, -1),   (1, -2),
            (-2, -1), (-1, -2),
        ]

    for (dr, dc) in d:
        nr = piece.r + dr
        nc = piece.c + dc

        if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                continue
        
        cap = board[nr][nc]
        if cap:
            if (cap.color != piece.color):
                captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=cap, promotion=False, enpassant=False, enpassant_cap=False))
        else:
            moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=None, promotion=False, enpassant=False, enpassant_cap=False))

    return (captures, moves)

def white_bishop_moves(piece:Piece, board: List[List[Piece]], prev_mv: Move) -> Tuple[List[Move], List[Move]]:
    moves = []
    captures = [] 

    # diagonal directions!
    d = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

    for (dr, dc) in d:
        nr = piece.r
        nc = piece.c

        while True:
            nr += dr
            nc += dc
            
            if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                break

            cap = board[nr][nc]
            # if there is a piece we will stop
            if cap:
                # but if there is a piece of other color here we can capture it
                if cap.color != piece.color:
                    captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=cap, promotion=False, enpassant=False, enpassant_cap=False))
                break
            else:
                # no piece we keep movin!
                moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=None, promotion=False, enpassant=False, enpassant_cap=False))

    return (captures, moves)

def white_rook_moves(piece:Piece, board: List[List[Piece]], prev_mv: Move) -> Tuple[List[Move], List[Move]]:
    moves = []
    captures = [] 

    # only verical/horizontal
    d = [(1, 0), (-1, 0), (0, -1), (0, 1)]

    for (dr, dc) in d:
        nr = piece.r
        nc = piece.c

        while True:
            nr += dr
            nc += dc
            
            if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLS:
                break

            cap = board[nr][nc]
            # if there is a piece we will stop
            if cap:
                # but if there is a piece of other color here we can capture it
                if cap.color != piece.color:
                    captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=cap, promotion=False, enpassant=False, enpassant_cap=False))
                break
            else:
                # no piece we keep movin!
                moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=None, promotion=False, enpassant=False, enpassant_cap=False))

    return (captures, moves)

def white_pawn_moves(piece:Piece, board: List[List[Piece]], prev_mv: Move) -> Tuple[List[Move], List[Move]]:
    moves = []
    captures = [] 

    nr = piece.r - 1 
    promotion = nr == 0
    if board[nr][piece.c] is None:
        if piece.r == 6:
            moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=piece.c, capture=None, promotion=promotion, enpassant=False, enpassant_cap=False))
            if board[nr-1][piece.c] is None:
                moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr-1, ce=piece.c, capture=None, promotion=promotion, enpassant=True, enpassant_cap=False))
        else:
            moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=piece.c, capture=None, promotion=promotion, enpassant=False, enpassant_cap=False))

    # check captures:
    for dc in [-1, 1]:
        nc = piece.c + dc
        if nc < 0 or nc >= COLS:
            break
        cap = board[nr][nc]
        if cap and (cap.color != piece.color):
            captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=cap, promotion=promotion, enpassant=False, enpassant_cap=False))

    return (captures, moves)

def black_pawn_moves(piece:Piece, board: List[List[Piece]], prev_mv: Move) -> Tuple[List[Move], List[Move]]:
    # prev_mv will never be None since black moves second
    moves = []
    captures = [] 
    
    nr = piece.r + 1
    if board[nr][piece.c] is None:
        if nr == ROWS-1:
            captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=piece.c, capture=None, promotion=False, enpassant=False, enpassant_cap=False))
        else:
            moves.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=piece.c, capture=None, promotion=False,enpassant=False, enpassant_cap=False))

    # check captures:
    for dc in [-1, 1]:
        nc = piece.c + dc
        if nc < 0 or nc >= COLS:
            break
        cap = board[nr][nc]
        if cap and (cap.color != piece.color):
            captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=cap, promotion=False, enpassant=False, enpassant_cap=False))
        
        if piece.r == 4:
            # if we can see enpassants 
            enpassant_cap = board[piece.r][nc]
            if enpassant_cap and (enpassant_cap.color != piece.color) and prev_mv.enpassant and enpassant_cap is prev_mv.piece:
                # if there is a piece adjacent of opposite color, check if the previous move was enpassant and if it was the piece to move
                captures.append(Move(piece=piece, rs=piece.r, cs=piece.c, re=nr, ce=nc, capture=enpassant_cap, promotion=False, enpassant=False, enpassant_cap=True))
    


    return (captures, moves)