import numpy as np
import copy


def square_opt(b, x, y):
    return b[9][0][x] | b[9][1][y] | b[9][2][x // 3 + (y // 3) * 3]


def square_opt_list(b, x, y):
    return [9-i for i, n in enumerate(np.binary_repr(square_opt(b, x, y), 9))
            if n == "0"]


def check(b, x, y, i):
    # Check Column, then Row, then Box
    if 2**(i-1) & (square_opt(b, x, y)) == 0:
        return True
    return False


def place(board, x, y, i):

    board[y][x] = i
    board[10].discard((x, y))

    # update sums of columns rows boxes
    board[9][0][x] += 2**(i - 1)
    board[9][1][y] += 2**(i - 1)
    board[9][2][x // 3 + (y // 3)*3] += 2**(i - 1)
    if board[9][0][x] | board[9][1][y] | board[9][2][x // 3 + (y // 3)*3] > 511:
        return np.empty(0)

    return board


def get_full(board):
    if len(board[10]) == 0:
        return True
    return False


def get_empty(board):
    min_opts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # board[10] is a set containing the co-ords of all the spaces yet to be filled
    for (x, y) in board[10]:
        opts = square_opt_list(board, x, y)
        if len(opts) == 0:
            return False
        if len(opts) == 1:
            return x, y, opts
        if len(min_opts) > len(opts):
            min_opts = opts
            min_coord = x, y

    if len(min_opts) == 10:
        return False

    return min_coord[0], min_coord[1], min_opts


def get_empty_low_opt(board):
    x, y = min(board[10], key=lambda coords: np.binary_repr(square_opt(board, coords[0], coords[1]), 9).count("0"))
    return x, y, square_opt_list(board, x, y)


def solve(board, n):
    n[0] += 1
    if board:
        if get_full(board):
            return board
        if square := get_empty_low_opt(board):
            for i in square[2]:
                if check(board, square[0], square[1], i):
                    if solved := solve(place(board, square[0], square[1], i), n):
                        return solved
                    else:
                        board[square[1]][square[0]] = 0
                        board[10].add((square[0], square[1]))
                        board[9][0][square[0]] -= 2**(i - 1)
                        board[9][1][square[1]] -= 2**(i - 1)
                        board[9][2][square[0] // 3 + (square[1] // 3)*3] -= 2**(i - 1)


