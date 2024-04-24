import copy
import math
from functools import lru_cache

class Board:
    def __init__(self, board):
        self.board = board

    def place(self, x, y, i):
        self.board[y][x] = i

    # Returns 0 indexed row
    def get_row(self, y):
        return self.board[y]

    # Returns 0 indexed column
    def get_column(self, x):
        return [self.board[i][x] for i in range(9)]

    # Returns 0 indexed box(Left->Right, Top->Bottom)
    # Returned box 1d array with order: (Left->Right, Top->Bottom)
    def get_box(self, i):
        box = []
        x = i % 3
        y = math.floor(i / 3)
        for cell_x in range(3):
            for cell_y in range(3):
                box.append(self.board[(y * 3) + cell_y][(x * 3) + cell_x])
        return box

    def check_valid(self):
        # Check all the rows
        rows = [self.get_row(y) for y in range(9)]
        for row in rows:
            for i in range(1, 10):
                if row.count(i) > 1:
                    return False

        # Check all the columns
        columns = [self.get_column(x) for x in range(9)]
        for column in columns:
            for i in range(1, 10):
                if column.count(i) > 1:
                    return False

        # Check all the boxes
        boxes = [self.get_box(i) for i in range(9)]
        for box in boxes:
            for i in range(1, 10):
                if box.count(i) > 1:
                    return False

        return True

    # Checks for any "0"s on the board
    # (They represent unfilled squares
    def check_full(self):
        rows = [self.get_row(y) for y in range(9)]
        for row in rows:
            if row.count(0) > 0:
                return False
        print("board is full")
        return True


start_board = [[0 for y in range(9)] for x in range(9)]
for i in range(9):
    row = input("enter a row\n")
    for index, num in enumerate(row.split(",")):
        if num != "0":
            start_board[i][index] = int(num)


@lru_cache()
def solver(board_tuple, n):
    n[0] += 1
    board = Board(board_tuple)
    if not board.check_valid():
        return

    for x in range(9):
        for y in range(9):
            if board.board[y][x] == 0:
                for i in range(1, 10):
                    # print("Checked square: (" + str(x) + ", " + str(y) + ") with number:", i)
                    new_board = Board(copy.deepcopy(board.board))
                    new_board.place(x, y, i)
                    answer = solver(new_board, n)
                    if answer:
                        if answer.check_full() and answer.check_valid():
                            return answer


n = [0]
for y in range(9):
    start_board[y] = tuple(start_board[y])
start_board = tuple(start_board)

b = solver(start_board, n)
print(n)
for row in b.board:
    print(row)


