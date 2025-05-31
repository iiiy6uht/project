import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Window setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.king = False
        self.calc_position()

    def calc_position(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw(self, win):
        pygame.draw.circle(win, BLACK, (self.x, self.y), SQUARE_SIZE // 2 - self.PADDING + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), SQUARE_SIZE // 2 - self.PADDING)
        if self.king:
            pygame.draw.circle(win, BLUE, (self.x, self.y), SQUARE_SIZE // 4)

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_position()

    def make_king(self):
        self.king = True


def draw_board(win):
    win.fill(BLACK)
    for row in range(ROWS):
        for col in range(row % 2, COLS, 2):
            pygame.draw.rect(win, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def create_pieces():
    pieces = []
    for row in range(ROWS):
        if row < 3:  # Top rows for red pieces
            color = RED
        elif row > 4:  # Bottom rows for white pieces
            color = WHITE
        else:
            continue

        for col in range(COLS):
            if (row + col) % 2 == 1:  # Only on black squares
                pieces.append(Piece(row, col, color))
    return pieces


def draw(win, pieces):
    draw_board(win)
    for piece in pieces:
        piece.draw(win)
    pygame.display.update()


def valid_move(piece, row, col):
    if piece.row == row and piece.col == col:
        return False  # Don't move to the same position
    if row < 0 or row >= ROWS or col < 0 or col >= COLS:
        return False  # Out of bounds
    if (row + col) % 2 == 0:
        return False  # Can only move to black squares
    return True


def main():
    run = True
    clock = pygame.time.Clock()
    pieces = create_pieces()
    selected_piece = None

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row = mouse_y // SQUARE_SIZE
                clicked_col = mouse_x // SQUARE_SIZE

                # Select a piece
                for piece in pieces:
                    if piece.row == clicked_row and piece.col == clicked_col:
                        selected_piece = piece
                        break

            if event.type == pygame.MOUSEMOTION:
                if selected_piece:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    selected_piece.calc_position()

            if event.type == pygame.MOUSEBUTTONUP:
                if selected_piece:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    new_row = mouse_y // SQUARE_SIZE
                    new_col = mouse_x // SQUARE_SIZE

                    if valid_move(selected_piece, new_row, new_col):
                        selected_piece.move(new_row, new_col)

                        # Promote to king if reaching the last row
                        if selected_piece.color == RED and selected_piece.row == 0:
                            selected_piece.make_king()
                        elif selected_piece.color == WHITE and selected_piece.row == ROWS - 1:
                            selected_piece.make_king()

                    selected_piece = None

        draw(WIN, pieces)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()