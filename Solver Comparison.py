import copy
from collections import namedtuple
from timeit import default_timer as timer
import numpy as np
import BitwiseSolver
import ClassesBack
import SudokuSolverExpensive
import SudokuSolverCheap
import FreshSolver
import Revolution

int_board = [[0, 0, 2, 0, 0, 7, 0, 0, 0],
             [0, 6, 0, 9, 0, 0, 4, 0, 0],
             [0, 9, 0, 2, 5, 0, 0, 0, 3],
             [0, 0, 0, 4, 0, 0, 1, 0, 0],
             [7, 3, 0, 0, 6, 0, 0, 0, 0],
             [0, 0, 9, 5, 3, 0, 0, 6, 0],
             [0, 0, 6, 3, 4, 0, 0, 7, 0],
             [8, 0, 0, 0, 0, 0, 0, 0, 9],
             [0, 0, 0, 0, 0, 0, 0, 5, 0]]

set_board = [[set(range(1, 10)) if x == 0 else x for x in row] for row in int_board]

np_board = copy.deepcopy(int_board)

# 0 representing binary number's length 9 here
# INDEX GUIDE:
#   0: Columns
#   1: Rows
#   2: Boxes


AM = np.array([[0 for x in range(9)] for a in range(3)], np.uint16)
# Fill Availability Matrix
setlist = list()
for y in range(9):
    for x in range(9):
        if int_board[y][x] != 0:
            AM[0][x] += 2**(int_board[y][x] - 1)
            AM[1][y] += 2**(int_board[y][x] - 1)
            AM[2][x // 3 + (y // 3)*3] += 2**(int_board[y][x] - 1)
        else:
            setlist.append((x, y))


rev_board = copy.deepcopy(int_board)
rev_board.append(AM)
# rev_board.append(np.array(setlist, dtype=np.dtype("int,int")))
rev_board.append(setlist)

np_board.append(AM)

solution = [[3, 4, 2, 6, 8, 7, 9, 1, 5],
            [5, 6, 8, 9, 1, 3, 4, 2, 7],
            [1, 9, 7, 2, 5, 4, 6, 8, 3],
            [6, 8, 5, 4, 7, 9, 1, 3, 2],
            [7, 3, 4, 1, 6, 2, 5, 9, 8],
            [2, 1, 9, 5, 3, 8, 7, 6, 4],
            [9, 2, 6, 3, 4, 5, 8, 7, 1],
            [8, 5, 1, 7, 2, 6, 3, 4, 9],
            [4, 7, 3, 8, 9, 1, 2, 5, 6]]


def timeit(method, limit=1):
    def timed(*args, **kw):
        sum_time = 0
        cycles = 0
        while sum_time < limit:
            deepCopyKwargs = copy.deepcopy(kw)
            ts = timer()
            result = method(*args, **deepCopyKwargs)
            te = timer()
            sum_time += (te - ts)
            cycles += 1
        avg_time = sum_time / cycles
        n[0] //= cycles
        print("avg_time over", cycles, "cycles is:", avg_time)

        return result

    return timed


def clear(board, x, y):
    # Clear as option in relevant sets
    for y_coord in range(9):
        for x_coord in range(9):
            # (y // 3, x // 3 == y_coord // 3, x_coord // 3) checks if it's in the same box
            if y == y_coord or x == x_coord or ((y // 3, x // 3) == (y_coord // 3, x_coord // 3)):
                if not(x == x_coord and y == y_coord):
                    if board[y_coord][x_coord] == board[y][x]:
                        print("done")
                        return False
                if type(board[y_coord][x_coord]) == set:
                    board[y_coord][x_coord].discard(board[y][x])
                    if len(board[y_coord][x_coord]) == 0:
                        print("abort")
                        return False
                    if len(board[y_coord][x_coord]) == 1:
                        board[y_coord][x_coord] = board[y][x]


for y in range(9):
    for x in range(9):
        if type(set_board[y][x]) == int:
            clear(set_board, x, y)


setlist = set()
for y in range(9):
    for x in range(9):
        if type(set_board[y][x]) == set:
            setlist.add((x, y))

set_board.append(setlist)
np_board.append(setlist)
cycles = 100
sum_length = 0
n = [0]


@timeit
def cheap(board, n):
    return SudokuSolverCheap.solve(copy.deepcopy(board), n)


@timeit
def expensive(board, n):
    return SudokuSolverExpensive.solver(copy.deepcopy(board), n)


@timeit
def fresh(board, n):
    return FreshSolver.solve(copy.deepcopy(board), n)

@timeit
def bit_solve(board, n):
    return BitwiseSolver.solve(copy.deepcopy(board), n)


@timeit
def rev_solve(board, n):
    return Revolution.solve(copy.deepcopy(board), n)


@timeit
def class_solve(b, n):
    board = ClassesBack.Board()
    board.init(b)
    return ClassesBack.solve(copy.deepcopy(board), n)


board = []
print("cheap:")
board = cheap(int_board, n)

if board != solution:
    print("FAIL")

for row in board[:9]:
    print(row)
print("n =", n[0], "\n")
n[0] = 0
# ---------------------------- #

print("fresh:")
board = fresh(set_board, n)
if board[:9] != solution:
    print("FAIL")

for row in board[:9]:
    print(row)
print("n =", n[0])
n[0] = 0

# ---------------------------- #
print("bitwise:")
board = bit_solve(np_board, n)
if board[:9] != solution:
    print("FAIL")

for row in board[:9]:
    print(row)
print("n =", n[0])
n[0] = 0
# ---------------------------- #

print("Revolution:")
board = rev_solve(rev_board, n)
if board[:9] != solution:
    print("FAIL")

for row in board[:9]:
    print(row)
print("n =", n[0])
n[0] = 0



