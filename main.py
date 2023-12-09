import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)

WINDOW_WIDTH = 300
WINDOW_HEIGHT = 600

BLOCK_SIZE = 30

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [1]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 1], [1, 0]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1]],
]

SHAPES_COLORS = [CYAN, YELLOW, ORANGE, BLUE, GREEN, PURPLE, RED]


class Block:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color


class Piece:
    def __init__(self, shape, color):
        self.shape = shape
        self.color = color
        self.row = 0
        self.col = WINDOW_WIDTH // BLOCK_SIZE // 2 - len(shape[0]) // 2

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def move_down(self):
        self.row += 1

    def move_left(self):
        self.col -= 1

    def move_right(self):
        self.col += 1


def draw_block(row, col, color):
    pygame.draw.rect(screen, color, (col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_board(board):
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] is not None:
                draw_block(row, col, board[row][col].color)


def is_valid_move(piece, board, move):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col] == 1:
                new_row = piece.row + row + move[0]
                new_col = piece.col + col + move[1]
                if not (0 <= new_row < len(board) and 0 <= new_col < len(board[0])) or \
                        (board[new_row][new_col] is not None):
                    return False
    return True


def update_board(board, piece):
    for row in range(len(piece.shape)):
        for col in range(len(piece.shape[row])):
            if piece.shape[row][col] == 1:
                board[piece.row + row][piece.col + col] = Block(piece.row + row, piece.col + col, piece.color)


def clear_lines(board):
    lines_to_clear = [i for i, row in enumerate(board) if all(cell is not None for cell in row)]
    for line in lines_to_clear:
        del board[line]
        board.insert(0, [None] * (WINDOW_WIDTH // BLOCK_SIZE))
    return len(lines_to_clear)


# Основной цикл игры
def main():
    clock = pygame.time.Clock()
    game_over = False
    board = [[None] * (WINDOW_WIDTH // BLOCK_SIZE) for _ in range(WINDOW_HEIGHT // BLOCK_SIZE)]

    current_piece = Piece(random.choice(SHAPES), random.choice(SHAPES_COLORS))
    next_piece = Piece(random.choice(SHAPES), random.choice(SHAPES_COLORS))

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and is_valid_move(current_piece, board, (0, -1)):
                    current_piece.move_left()
                elif event.key == pygame.K_RIGHT and is_valid_move(current_piece, board, (0, 1)):
                    current_piece.move_right()
                elif event.key == pygame.K_DOWN and is_valid_move(current_piece, board, (1, 0)):
                    current_piece.move_down()
                elif event.key == pygame.K_UP:
                    rotated_piece = Piece(current_piece.shape, current_piece.color)
                    rotated_piece.row, rotated_piece.col = current_piece.row, current_piece.col
                    rotated_piece.rotate()
                    if is_valid_move(rotated_piece, board, (0, 0)):
                        current_piece = rotated_piece

        if is_valid_move(current_piece, board, (1, 0)):
            current_piece.move_down()
        else:
            update_board(board, current_piece)
            lines_cleared = clear_lines(board)
            if lines_cleared > 0:
                print(f"Lines cleared: {lines_cleared}")
            current_piece = next_piece
            next_piece = Piece(random.choice(SHAPES), random.choice(SHAPES_COLORS))
            if not is_valid_move(current_piece, board, (0, 0)):
                game_over = True

        screen.fill(BLACK)
        draw_board(board)
        draw_block(next_piece.row, next_piece.col, next_piece.color)
        for row in range(len(current_piece.shape)):
            for col in range(len(current_piece.shape[row])):
                if current_piece.shape[row][col] == 1:
                    draw_block(current_piece.row + row, current_piece.col + col, current_piece.color)

        pygame.display.flip()

        clock.tick(5)

    pygame.quit()


if __name__ == "__main__":
    main()
