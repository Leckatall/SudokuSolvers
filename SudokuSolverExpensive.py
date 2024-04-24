import copy

import numpy as np


class Board_v2:
    def __init__(self, board):
        self.board = board

    def can_place(self, x, y, i):
        return not(i in self.get_row(y) or
                   i in self.get_column(x) or
                   i in self.get_box(x, y))

    def place(self, x, y, i):
        self.board[y][x] = i

    def update_sets_2(self):
        for y in range(9):
            for x in range(9):
                if type(self.board[y][x]) == set:
                    self.board[y][x].difference_update(self.row_nums[y].union(self.column_nums[x], self.box_nums[y // 3][x // 3]))
                    if len(self.board[y][x]) == 0:
                        return False
                    if len(self.board[y][x]) == 1:
                        self.board[y][x] = list(self.board[y][x])[0]

        return True

    def update_sets(self):
        for y in range(9):
            for x in range(9):
                if type(self.board[y][x]) == set:
                    empty_cross = np.concatenate((self.board[y][:x],
                                                  self.board[y][x + 1:],
                                                  self.board[:y][x:x+1],
                                                  self.board[y + 1:][x:x+1]), axis=None)

                    box = self.get_box(x, y)
                    box.remove(self.board[y][x])
                    surround = np.concatenate((empty_cross, box), axis=None)
                    surround = [i for i in surround if type(i) == int]
                    self.board[y][x].difference_update(surround)

                    if len(self.board[y][x]) == 0:
                        return False
                    if len(self.board[y][x]) == 1:
                        self.board[y][x] = list(self.board[y][x])[0]
        return True

    def free_cell(self):
        for y in range(9):
            for x in range(9):
                if type(self.board[y][x]) == set:
                    return x, y
        return False

    # Returns 0 indexed row
    def get_row(self, y):
        return self.board[y]

    # Returns 0 indexed column
    def get_column(self, x):
        return [self.board[i][x] for i in range(9)]

    # Returned box 1d array with order: (Left->Right, Top->Bottom)
    def get_box(self, x, y):
        box = []
        box_x = x // 3
        box_y = y // 3

        for cell_y in range(3):
            for cell_x in range(3):
                box.append(self.board[(box_y * 3) + cell_y][(box_x * 3) + cell_x])
        return box


def solver(grid, n):
    n[0] += 1

    board = Board_v2(grid)

    if not board.update_sets():
        return False

    if not board.free_cell():
        print(board.board)
        return True

    x, y = board.free_cell()

    for i in board.board[y][x]:
        if board.can_place(x, y, i):
            new_board = Board_v2(copy.deepcopy(grid))
            new_board.place(x, y, i)
            answer = solver(new_board.board, n)
            if answer:
                return answer


if __name__ == "__main__":
    brd = [[0 for y in range(9)] for x in range(9)]
    for i in range(9):
        row = input("enter a row\n")
        for index, num in enumerate(row.split(",")):
            if num != "0":
                brd[i][index] = int(num)
    print("thx")

    start_board = brd

    n = [0]
    b = solver(start_board)
    print(n)



