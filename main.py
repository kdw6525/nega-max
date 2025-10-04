import pygame
import sys
import copy
from piece import Piece, black_pawn_evaluation, white_pawn_evaluation, white_knight_evaluation, white_bishop_evaluation, white_king_evaluation, white_rook_evaluation
from moves import Move, black_pawn_moves, white_pawn_moves, white_knight_moves, white_bishop_moves, white_king_moves, white_rook_moves
import random

pygame.init()

# Board size
BOARD_SIZE = 480
ROWS, COLS = 8, 5
SQUARE_SIZE = BOARD_SIZE // COLS

# Side panel size
PANEL_WIDTH = 150
WIDTH, HEIGHT = BOARD_SIZE + PANEL_WIDTH, SQUARE_SIZE * ROWS

# Colors
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
HIGHLIGHT = (0, 255, 0, 100)
PANEL_BG = (50, 50, 50)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER = (180, 180, 180)
TEXT_COLOR = (10, 10, 10)

# Load piece images
pieces = {}
piece_names = ['bp', 'wp', 'wr', 'wn', 'wb', 'wk']
for name in piece_names:
    pieces[name] = pygame.image.load(f'assets/{name}.png')
    pieces[name] = pygame.transform.scale(pieces[name], (SQUARE_SIZE, SQUARE_SIZE))

# Board initialization, populated when main is ran
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

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zerg Chess")

FONT = pygame.font.SysFont("arial", 20)

# Button rect
undo_button = pygame.Rect(BOARD_SIZE + 20, 40, PANEL_WIDTH - 40, 40)
ai_button = pygame.Rect(BOARD_SIZE + 20, 100, PANEL_WIDTH - 40, 40)

# Utility functions

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
    king = Piece(id=i, r=0, c=0, color=True, png='wk', 
                 move_generator=white_king_moves, 
                 evaluation_function=white_king_evaluation)
    piece_lst[i] = king

    knight = Piece(id=i+1, r=0, c=0, color=True, png='wn', 
                   move_generator=white_knight_moves, 
                   evaluation_function=white_knight_evaluation)
    piece_lst[i+1] = knight

    bishop = Piece(id=i+2, r=0, c=0, color=True, png='wb', 
                   move_generator=white_bishop_moves, 
                   evaluation_function=white_bishop_evaluation)
    piece_lst[i+2] = bishop

    rook = Piece(id=i+3, r=0, c=0, color=True, png='wr', 
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
            board[7][c] = king
            c+=1
            continue
        if char == "n":
            board[7][c] = knight
            c+=1
            continue
        if char == "b":
            board[7][c] = bishop
            c+=1
            continue
        if char == "r":
            board[7][c] = rook
            c+=1
            continue

    return

def draw_board(win):
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                win.blit(pieces[piece.png], (col*SQUARE_SIZE, row*SQUARE_SIZE))

def draw_panel(win):
    pygame.draw.rect(win, PANEL_BG, (BOARD_SIZE, 0, PANEL_WIDTH, HEIGHT))

    # Draw Undo button
    mouse = pygame.mouse.get_pos()
    if undo_button.collidepoint(mouse):
        pygame.draw.rect(win, BUTTON_HOVER, undo_button)
    else:
        pygame.draw.rect(win, BUTTON_COLOR, undo_button)

    text = FONT.render("Undo", True, TEXT_COLOR)
    win.blit(text, (undo_button.x + (undo_button.width - text.get_width()) // 2,
                    undo_button.y + (undo_button.height - text.get_height()) // 2))
    
    if ai_button.collidepoint(mouse):
        pygame.draw.rect(win, BUTTON_HOVER, ai_button)
    else:
        pygame.draw.rect(win, BUTTON_COLOR, ai_button)

    text = FONT.render("AI Move", True, TEXT_COLOR)
    win.blit(text, (ai_button.x + (ai_button.width - text.get_width()) // 2,
                    ai_button.y + (ai_button.height - text.get_height()) // 2))


def get_square_under_mouse():
    x, y = pygame.mouse.get_pos()
    if x >= BOARD_SIZE:
        return None, None
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return row, col

def is_opponent(piece1: Piece, piece2: Piece):
    if piece1 is None or piece2 is None:
        return False
    return piece1.color != piece2.color

# Move generation
def valid_moves(board, row, col):
    piece = board[row][col]
    moves = []
    if piece == "":
        return moves
    color = piece[0]
    p = piece[1]

    directions = []
    if p == "p":  # Pawn
        direction = -1 if color == "w" else 1
        start_row = 6 if color == "w" else 1
        if 0 <= row+direction < ROWS and board[row+direction][col] == "":
            moves.append((row+direction, col))
            if row == start_row and board[row+2*direction][col] == "":
                moves.append((row+2*direction, col))
        for dc in [-1, 1]:
            nr, nc = row+direction, col+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and is_opponent(piece, board[nr][nc]):
                moves.append((nr, nc))

    elif p == "r":  # Rook
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
    elif p == "b":  # Bishop
        directions = [(1,1), (-1,-1), (1,-1), (-1,1)]
    elif p == "q":  # Queen
        directions = [(1,0), (-1,0), (0,1), (0,-1), (1,1), (-1,-1), (1,-1), (-1,1)]
    elif p == "k":  # King
        for dr in [-1,0,1]:
            for dc in [-1,0,1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row+dr, col+dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and (board[nr][nc] == "" or is_opponent(piece, board[nr][nc])):
                    moves.append((nr, nc))
    elif p == "n":  # Knight
        jumps = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for dr, dc in jumps:
            nr, nc = row+dr, col+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and (board[nr][nc] == "" or is_opponent(piece, board[nr][nc])):
                moves.append((nr, nc))

    for dr, dc in directions:
        nr, nc = row+dr, col+dc
        while 0 <= nr < ROWS and 0 <= nc < COLS:
            if board[nr][nc] == "":
                moves.append((nr, nc))
            elif is_opponent(piece, board[nr][nc]):
                moves.append((nr, nc))
                break
            else:
                break
            nr += dr
            nc += dc

    return moves

def promote_pawns(board):
    for col in range(COLS):
        if board[0][col] == "wp":
            board[0][col] = "wq"
        if board[7][col] == "bp":
            board[7][col] = "bq"

def main():
    fill_board()
    clock = pygame.time.Clock()
    selected = None
    legal_moves = []
    turn = True  # White starts

    history = [copy.deepcopy(board)]  # store board states

    run = True
    while run:
        draw_board(WIN)
        draw_pieces(WIN, board)
        draw_panel(WIN)

        # Highlight moves
        legal_destinations = [(mv.re, mv.ce) for mv in legal_moves]
        for r, c in legal_destinations:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(HIGHLIGHT)
            WIN.blit(s, (c*SQUARE_SIZE, r*SQUARE_SIZE))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if undo_button.collidepoint(event.pos):
                    if len(history) > 1:
                        history.pop()
                        prev_state = history[-1]
                        for r in range(8):
                            for c in range(5):
                                board[r][c] = prev_state[r][c]
                        turn = not turn  # reverse turn
                    continue

                row, col = get_square_under_mouse()
                if row is None:  # clicked panel
                    continue
                piece = board[row][col]

                if selected:
                    if (row, col) in legal_destinations:
                        mv_piece = board[selected[0]][selected[1]]
                        mv_piece.r, mv_piece.c = row, col
                        board[row][col] = mv_piece
                        board[selected[0]][selected[1]] = None
                        promote_pawns(board)
                        history.append(copy.deepcopy(board))  # save state
                        turn = not turn
                    selected, legal_moves = None, []
                else:
                    if piece and piece.color == turn:
                        selected = (row, col)
                        legal_moves = piece.get_moves(board)
                        legal_moves = legal_moves[0] + legal_moves[1]

if __name__ == "__main__":
    main()
