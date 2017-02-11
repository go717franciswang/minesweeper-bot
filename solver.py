EMPTY = 0
ONE = 1
TWO = 2
THREE = 3
FOUR = 4
FIVE = 5
SIX = 6
SEVEN = 7
EIGHT = 8
BOMB = 9
HIDDEN = 10
NUMBER = 11

def char2box(char):
    if char == '_':
        return HIDDEN
    else:
        return int(char)

class Board:
    def __init__(self, board_matrix, w, h):
        self.board_matrix = board_matrix
        self.w = w
        self.h = h
        self.revealed = False

    def each_number_box(self):
        for i in xrange(len(self.board_matrix)):
            if self.board_matrix[i] < 9:
                yield (i//self.w, i%self.w), self.board_matrix[i]

    def hidden_around(self, pos):
        return [p for p in self.around(pos) if self[p] == HIDDEN]

    def bombs_around(self, pos):
        return [p for p in self.around(pos) if self[p] == BOMB]

    def around(self, pos):
        r, c = pos
        for dr in xrange(-1,2):
            if r+dr<0 or r+dr>=self.h:
                continue
            for dc in xrange(-1,2):
                if dr==0 and dc==0:
                    continue
                if c+dc<0 or c+dc>=self.w:
                    continue
                yield (r+dr, c+dc)

    def __getitem__(self, pos):
        r, c = pos
        return self.board_matrix[r*self.w+c]

    def __setitem__(self, pos, value):
        r, c = pos
        self.board_matrix[r*self.w+c] = value
        self.revealed = True

class Solver:
    def __init__(self, board):
        self.board = board
        self.revealed_numbers = []

    def solve(self):
        for pos, n in self.board.each_number_box():
            hiddens = self.board.hidden_around(pos)
            bombs = self.board.bombs_around(pos)
            if len(hiddens) == n-len(bombs):
                for p in hiddens:
                    self.board[p] = BOMB

            if n-len(bombs) == 0:
                for p in hiddens:
                    self.board[p] = NUMBER
                    self.revealed_numbers.append(p)

        if self.board.revealed:
            self.board.revealed = False
            return self.solve()

    @staticmethod
    def from_string(s, w, h):
        board = Board([char2box(c) for c in s if c != '\n'], w, h)
        return Solver(board)

