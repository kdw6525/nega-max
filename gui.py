import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
ROWS, COLS = 8, 5
WIDTH = 480
SQUARE_SIZE = WIDTH // COLS
HEIGHT = SQUARE_SIZE * ROWS

# Colors
WHITE = (245, 245, 245)
BLACK = (30, 30, 30)
GREEN = (0, 255, 0)

# Load piece images
pieces = {}
piece_names = ['bp', 'wp', 'wr', 'wn', 'wb', 'wk']
for name in piece_names:
    pieces[name] = pygame.image.load(f'assets/{name}.png')
    pieces[name] = pygame.transform.scale(pieces[name], (SQUARE_SIZE, SQUARE_SIZE))

# Board setup
board = [
    ["bp"] * 5,
    ["bp"] * 5,
    ["bp"] * 5,
    [""] * 5,
    [""] * 5,
    [""] * 5,
    ["wp"] * 5,
    ["", "wk", "wb", "wn", "wr"]
]

# Create the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

def draw_board(win):
    win.fill(WHITE)
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(win, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(win, board):
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                win.blit(pieces[piece], (col*SQUARE_SIZE, row*SQUARE_SIZE))

def get_square_under_mouse():
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    clock = pygame.time.Clock()
    selected_piece = None
    selected_pos = None

    run = True
    while run:
        draw_board(WIN)
        draw_pieces(WIN, board)
        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_under_mouse()
                if selected_piece:
                    # Move piece
                    board[row][col] = selected_piece
                    board[selected_pos[0]][selected_pos[1]] = ""
                    selected_piece = None
                    selected_pos = None
                elif board[row][col] != "":
                    # Select piece
                    selected_piece = board[row][col]
                    selected_pos = (row, col)

if __name__ == "__main__":
    main()