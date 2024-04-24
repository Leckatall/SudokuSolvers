import copy
import math

board = [[0 for y in range(9)] for x in range(9)]
for i in range(9):
    row = input("enter a row\n")
    for index, num in enumerate(row.split(",")):
        if num != "0":
            board[i][index] = int(num)


def next_square(b):
    for y in range(9):
        for x in range(9):
            if b[y][x] == 0:
                return x, y

    return False


def is_valid(b, num, pos):
    x, y = pos
    # Check row
    for i in range(len(b[0])):
        if b[y][i] == num:
            return False

    # Check the column
    for i in range(len(b)):
        if b[i][x] == num:
            return False

    # Check box
    box_x = x // 3
    box_y = y // 3
    for cell_x in range(3):
        for cell_y in range(3):
            if b[(box_y * 3) + cell_y][(box_x * 3) + cell_x] == num:
                return False
    return True


def print_board(b):
    for row in b:
        print(row)


def solve(b):
    n[0] += 1
    square = next_square(b)
    if not square:
        print("gj you won")
        print_board(b)
        return True
    x, y = square

    for i in range(1, 10):
        if is_valid(b, i, (x, y)):
            b[y][x] = i
            if solve(b):
                return True
            b[y][x] = 0


n = [0]
solve(board)
print("n:", n[0])


