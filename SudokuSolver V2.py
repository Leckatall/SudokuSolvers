
class Board_v2:
    def __init__(self, board):
        self.board = board

    def can_place(self, x, y, i):
        placable = not(i in self.get_row(y) or
                   i in self.get_column(x) or
                   i in self.get_box(x, y))
        return placable

    def free_cell(self):
        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
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


def solver(grid):
    n[0] += 1

    board = Board_v2(grid)

    if not board.free_cell():
        print("win")
        return board

    x, y = board.free_cell()
    for i in range(1, 10):
        if board.can_place(x, y, i):
            board.board[y][x] = i
            answer = solver(board.board)
            if answer:
                return answer
            board.board[y][x] = 0


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
    for row in b.board:
        print(row)


