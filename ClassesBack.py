import numpy as np
from queue import PriorityQueue


class Board:
    def init(self, board):
        self.board = board

    def place(self, x, y, i):
        self.board[y][x] = i

        # Remove from writable cells
        print(self.board[10][0])
        print(type(self.board[10][0]))
        if self.board[10][0] == (x, y):
            self.board[10] = np.delete(self.board[10], 0)
        else:
            print("failed idk why")

        # Update sums of Columns, Rows and Boxes
        self.board[9][0][x] += 2**(i - 1)
        self.board[9][1][y] += 2**(i - 1)
        self.board[9][2][x // 3 + (y // 3)*3] += 2**(i - 1)

    def get_empty(self):
        print("\ngetting empty")
        print(self.board[:-2])
        print("summation_check Vs self.board.verifies")
        print(self.board[9][self.board[9] != self.summation_check()])

        # board[10] is a set containing the co-ords of all the spaces yet to be filled
        print(self.board[10])
        setlist_opts = list()
        for cell in self.board[10]:
            setlist_opts.append(self.square_opt_count(cell))

        self.board[10] = self.board[10][np.argsort(setlist_opts)]
        x, y = self.board[10][0]
        if np.binary_repr(self.square_opt(x, y), 9).count("0") == 0:
            print("CANCEL TREE")
            return False
        print("x: %s, y: %s" % (x, y))
        return x, y, self.square_opt_list(x, y)

    def get_full(self):
        if len(self.board[10]) == 0:
            return True
        return False

    def summation_check(self):
        AM = np.array([[0 for x in range(9)] for a in range(3)], np.uint16)
        # Fill Availability Matrix
        setlist = list()
        for y in range(9):
            for x in range(9):
                if self.board[y][x] != 0:
                    AM[0][x] += 2**(self.board[y][x] - 1)
                    AM[1][y] += 2**(self.board[y][x] - 1)
                    AM[2][x // 3 + (y // 3)*3] += 2**(self.board[y][x] - 1)
                else:
                    setlist.append((x, y))
        return AM

    def square_opt(self, x, y):
        return self.board[9][0][x] | self.board[9][1][y] | self.board[9][2][x // 3 + (y // 3) * 3]

    def square_opt_list(self, x, y):
        return [9-i for i, n in enumerate(np.binary_repr(self.square_opt(x, y), 9)) if n == "0"]

    def square_opt_count(self, cell):
        return np.binary_repr(self.square_opt(cell[0], cell[1]), 9).count("0")

    def remove(self, x, y, i):
        self.board[y][x] = 0

        # Remove from writable cells
        self.board[10] = np.append(self.board[10], np.array((x, y), dtype=np.dtype("int,int")))

        # Update sums of Columns, Rows and Boxes
        self.board[9][0][x] -= 2**(i - 1)
        self.board[9][1][y] -= 2**(i - 1)
        self.board[9][2][x // 3 + (y // 3)*3] -= 2**(i - 1)


# def get_empty_vQ(board):
#     # board[10] is a set containing the co-ords of all the spaces yet to be filled
#     print(board[10])
#     q = PriorityQueue()
#     for cell in board[10]:
#         q.put((square_opt_count(board, cell), cell))
#
#     returning_item = q.get()
#     x, y = returning_item[1]
#     if returning_item[0] == 0:
#         return False
#     return x, y, square_opt_list(board, x, y)


def solve(board, n):
    n[0] += 1
    if board.get_full():
        return board
    if square := board.get_empty():
        for i in square[2]:
            board.place(square[0], square[1], i)
            if solved := solve(board, n):
                return solved
            else:
                board.remove(square[0], square[1], i)


