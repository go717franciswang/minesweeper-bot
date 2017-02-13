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

    def clone(self):
        return Board([x for x in self.board_matrix], self.w, self.h)

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

class Contradiction(Exception):
    pass

class Solver:
    def __init__(self, board):
        self.board = board
        self.revealed_numbers = []
        self.revealed_bombs = []

    def solve(self):
        revealed_count = len(self.revealed_numbers)
        self.naive_solve()
        self.conjecture_solve()
        if len(self.revealed_numbers) > revealed_count:
            self.solve()

    def naive_solve(self):
        for pos, n in self.board.each_number_box():
            hiddens = self.board.hidden_around(pos)
            bombs = self.board.bombs_around(pos)
            if len(hiddens) == n-len(bombs):
                for p in hiddens:
                    self.reveal_bomb(p)

            if n-len(bombs) == 0:
                for p in hiddens:
                    self.reveal_number(p)

            if len(bombs) > n:
                raise Contradiction()

    def reveal_number(self, p):
        self.board[p] = NUMBER
        self.revealed_numbers.append(p)

    def reveal_bomb(self, p):
        self.board[p] = BOMB
        self.revealed_bombs.append(p)

    def conjecture_solve(self):
        # for each box
        #     for each surrounding box, assume it's bomb, and naive solve
        #     from each conjecture's result set, if a box has the same result from every conjecture, then it must be true
        for pos, n in self.board.each_number_box():
            hiddens = self.board.hidden_around(pos)
            bomb_candidates = None
            number_candidates = None
            for hidden_pos in hiddens:
                s = self.fresh_solver()
                s.board[hidden_pos] = BOMB
                try:
                    s.naive_solve()
                except Contradiction:
                    self.reveal_number(hidden_pos)
                    continue

                if bomb_candidates is None:
                    bomb_candidates = set(s.revealed_bombs)
                    number_candidates = set(s.revealed_numbers)
                else:
                    bomb_candidates.intersection_update(set(s.revealed_bombs))
                    number_candidates.intersection_update(set(s.revealed_numbers))

            for p in bomb_candidates or []:
                self.reveal_bomb(p)
            for p in number_candidates or []:
                self.reveal_number(p)

    def backtrack_solve(self, depth):
        # for each edge box
        #     assume it's bomb, if we reach a contradiction, then it must be number
        #     assume it's number, if we reach a contradiction, then it must be bomb
        pass

    @staticmethod
    def from_string(s, w, h):
        board = Board([char2box(c) for c in s if c != '\n'], w, h)
        return Solver(board)

    def fresh_solver(self):
        return Solver(self.board.clone())

