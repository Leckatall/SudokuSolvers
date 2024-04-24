import numpy as np
from queue import PriorityQueue


def square_opt(b, x, y):
    return b[9][0][x] | b[9][1][y] | b[9][2][x // 3 + (y // 3) * 3]


def square_opt_list(b, x, y):
    return [9-i for i, n in enumerate(np.binary_repr(square_opt(b, x, y), 9))
            if n == "0"]


def square_opt_count(b, cell):
    return np.binary_repr(square_opt(b, cell[0], cell[1]), 9).count("0")


def place(board, x, y, i):
    board[y][x] = i

    # Remove from writable cells
    board[10].remove((x, y))

    # Update sums of Columns, Rows and Boxes
    board[9][0][x] += 2**(i - 1)
    board[9][1][y] += 2**(i - 1)
    board[9][2][x // 3 + (y // 3)*3] += 2**(i - 1)


def get_full(board):
    if len(board[10]) == 0:
        return True
    return False


def get_empty(board):
    # board[10] is a set containing the co-ords of all the spaces yet to be filled
    x, y = min(board[10], key=lambda a: square_opt_count(board, a))
    if np.binary_repr(square_opt(board, x, y), 9).count("0") == 0:
        return False
    return x, y, square_opt_list(board, x, y)


def solve(board, n):
    n[0] += 1
    if get_full(board):
        return board
    if square := get_empty(board):
        for i in square[2]:
            place(board, square[0], square[1], i)
            if solved := solve(board, n):
                return solved
            else:
                board[square[1]][square[0]] = 0
                board[10].append((square[0], square[1]))
                board[9][0][square[0]] -= 2**(i - 1)
                board[9][1][square[1]] -= 2**(i - 1)
                board[9][2][square[0] // 3 + (square[1] // 3)*3] -= 2**(i - 1)


