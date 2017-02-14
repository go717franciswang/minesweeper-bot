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
    return int(char)

def box2char(box):
    if box == HIDDEN:
        return '_'
    if box == NUMBER:
        return 'N'
    if box == BOMB:
        return '*'
    return str(box)

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

    def to_string(self):
        s = ""
        for r in xrange(self.h):
            for c in xrange(self.w):
                s += box2char(self[(r,c)])
            s += "\n"
        return s

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
        self.guess_pos = None
        self.guess_prob = None

    def solve(self):
        revealed_count = len(self.revealed_numbers)
        self.naive_solve()
        self.conjecture_solve()
        if len(self.revealed_numbers) > revealed_count:
            return self.solve()

        if len(self.revealed_numbers) == 0:
            self.guess()

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

    def guess(self):
        box_chance = {}
        for pos, n in self.board.each_number_box():
            hiddens = self.board.hidden_around(pos)
            if len(hiddens) == 0:
                continue

            bombs = self.board.bombs_around(pos)
            m = float(n-len(bombs))/len(hiddens)
            for p in hiddens:
                box_chance.setdefault(p, [])
                box_chance[p].append(m)

        box_score = []
        for p, chances in box_chance.iteritems():
            box_score.append((p, len(chances)/sum(1/x for x in chances)))
        self.guess_pos, self.guess_prob = sorted(box_score, key=lambda x: x[1])[0]

    @staticmethod
    def from_string(s, w, h):
        board = Board([char2box(c) for c in s if c != '\n'], w, h)
        return Solver(board)

    def fresh_solver(self):
        return Solver(self.board.clone())

    def to_string(self):
        s = self.board.to_string()
        if self.guess_prob:
            r,c = self.guess_pos
            i = r*(self.board.w+1)+c
            s = s[:i]+'?'+s[i+1:]
        return s

