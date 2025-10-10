import pygame
import sys
import numpy as np
from piece import Piece
from moves import Move
from board import fill_board, make_board_move, undo_board_move, board, BOARD_SIZE, COLS, ROWS
from search import nega_max_root

pygame.init()

# Board size
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

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zerg Chess")

FONT = pygame.font.SysFont("arial", 20)

# Button rect
undo_button = pygame.Rect(BOARD_SIZE + 20, 40, PANEL_WIDTH - 40, 40)
ai_button = pygame.Rect(BOARD_SIZE + 20, 100, PANEL_WIDTH - 40, 40)

# Utility functions

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

# search the list and return if there is a move with the end pos (r, c)
def find_mv(r, c, mvs):
    # iterate through moves
    for mv in mvs:
        if r == mv.re and c == mv.ce:
            return mv
    return None
    

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

    history = []  # no moves to undo

    run = True
    while run:
        draw_board(WIN)
        draw_pieces(WIN, board)
        draw_panel(WIN)

        # Highlight moves
        for mv in legal_moves:
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            s.fill(HIGHLIGHT)
            WIN.blit(s, (mv.ce*SQUARE_SIZE, mv.re*SQUARE_SIZE))

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if undo_button.collidepoint(event.pos):
                    if history:
                        undo_board_move(mv=history.pop())
                        turn = not turn  # reverse turn
                    continue

                if ai_button.collidepoint(event.pos):
                    # TODO, execute ai move
                    prev_move = None
                    if history:
                        prev_move = history[-1]
                    # make depth odd so the first player doesn't do something dumb
                    ai_mv = nega_max_root(prev_move=prev_move, d=5, alpha=-1000, beta=1000, turn=turn)
                    if ai_mv:
                        make_board_move(mv=ai_mv)
                        history.append(ai_mv)
                        turn = not turn
                    # reset selection
                    selected, legal_moves = None, []
                    continue

                row, col = get_square_under_mouse()
                if row is None:  # clicked panel
                    continue
                piece = board[row][col]

                if selected:
                    mv = find_mv(r=row, c=col, mvs=legal_moves)
                    if mv:
                        make_board_move(mv=mv)
                        history.append(mv)  # save move
                        turn = not turn
                    selected, legal_moves = None, []
                else:
                    if piece and piece.color == turn:
                        selected = (row, col)
                        legal_moves = piece.get_moves(board, history[-1] if len(history) != 0 else None)
                        legal_moves = legal_moves[0] + legal_moves[1]

if __name__ == "__main__":
    main()
