import math


class Board:
    def __init__(self):
        self.board = [[set(range(1, 10)) for y in range(9)] for x in range(9)]
        for i in range(9):
            row = input("enter a row\n")
            for index, num in enumerate(row.split(",")):
                if num != "0":
                    self.board[i][index] = int(num)

    def check_cell(self, x, y):
        if type(self.board[y][x]) != int:
            if len(self.board[y][x]) == 1:
                self.board[y][x] = list(self.board[y][x])[0]
            else:
                self.check_cell_row(x, y)
                self.check_cell_column(x, y)
                self.check_cell_box(x, y)

    def check_cell_row(self, x, y):
        for cell in self.board[y]:
            if type(cell) == int:
                self.discard(cell, x, y)

    def check_cell_column(self, x, y):
        for row in self.board:
            if type(row[x]) == int:
                self.discard(row[x], x, y)

    def check_cell_box(self, x, y):
        box = math.floor(x / 3), math.floor(y / 3)
        for cell_x in range(3):
            for cell_y in range(3):
                cell = self.board[cell_y + (box[1] * 3)][cell_x + (box[0] * 3)]
                if type(cell) == int:
                    self.discard(cell, x, y)

    def discard(self, cell, x, y):
        if type(self.board[y][x]) != int:
            if len(self.board[y][x]) == 1:
                print("should not have attempted a discard")
                print("x:", x, "y:", y)
                self.board[y][x] = list(self.board[y][x])[0]
            else:
                self.board[y][x].discard(cell)

                if len(self.board[y][x]) == 1:
                    self.board[y][x] = list(self.board[y][x])[0]

    def place(self, x, y):
        if type(self.board[y][x]) != int:
            for num in self.board[y][x]:
                if self.can_place(num, x, y):
                    self.board[y][x] = num
                    print("placed")

    def can_place(self, num, x, y):
        # check row
        for index, cell in enumerate(self.board[y]):
            if type(cell) != int:
                if num in cell:
                    if index != x:
                        return False

        # check column
        for index, row in enumerate(self.board):
            if type(row[x]) != int:
                if num in row[x]:
                    if index != y:
                        return False

        # check box
        box = math.floor(x / 3), math.floor(y / 3)
        for cell_x in range(3):
            for cell_y in range(3):
                cell = self.board[cell_y + (box[1] * 3)][cell_x + (box[0] * 3)]
                if type(cell) != int:
                    if num in cell:
                        if cell_y + (box[1] * 3) != y or cell_x + (box[0] * 3) != x:
                            return False

        return True


if __name__ == "__main__":
    board = Board()

    for _ in range(1000):
        for x in range(9):
            for y in range(9):
                board.check_cell(x, y)
                board.place(x, y)

    for row in board.board:

        print((str(row)[1:-1]).replace(" ", ""))






