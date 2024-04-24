import copy
from functools import lru_cache
import numpy as np


def check(b, x, y, i):
    if type(b[y][x]) != set:
        print("wut")
    for y_coord in range(9):
        for x_coord in range(9):
            if y == y_coord or x == x_coord or (y // 3 == y_coord // 3 and x // 3 == x_coord // 3):
                if not(x == x_coord and y == y_coord):
                    if b[y_coord][x_coord] == i:
                        return False
    return True


def place(b, x, y, i, n):
    n[0] += 1
    if type(b) == bool:
        print(b)
        return False
    board = copy.deepcopy(b)

    board[y][x] = i
    board[9].discard((x, y))

    clearlist = set()
    for z in range(9):
        clearlist.add((z, y))
        clearlist.add((x, z))
        clearlist.add((((x // 3)*3) + z % 3, ((y // 3)*3) + z // 3))
    clearlist.intersection_update(board[9])

    # Clear as option in relevant sets
    for cell in clearlist:
        x_coord, y_coord = cell
        # (y // 3, x // 3 == y_coord // 3, x_coord // 3) checks if it's in the same box
        if type(board[y_coord][x_coord]) == set:
            board[y_coord][x_coord].discard(i)
            if len(board[y_coord][x_coord]) == 0:
                return False
            if len(board[y_coord][x_coord]) == 1:
                if not check(board, x_coord, y_coord, list(board[y_coord][x_coord])[0]):
                    return False
                if not (board := place(board, x_coord, y_coord, board[y_coord][x_coord].pop(), n)):
                    return False

    return board


def get_empty(board):
    square = False
    min_length = 10
    for coord in board[9]:
        if min_length > len(board[coord[1]][coord[0]]):
            min_length = len(board[coord[1]][coord[0]])
            min_coord = coord[0], coord[1]
            square = True

    if not square:
        return False
    return min_coord[0], min_coord[1], board[min_coord[1]][min_coord[0]]


def solve(board, n):
    if board:
        square = get_empty(board)
        if not square:
            return board
        for i in square[2].copy():
            if check(board, square[0], square[1], i):
                if solved := solve(place(board, square[0], square[1], i, n), n):
                    return solved

