from solver import Solver
import time
happy_face = find("Screen Shot 2017-02-09 at 4.11.06 PM.png").getTarget()
box_patterns = {
        '0': Pattern("Screen Shot 2017-02-09 at 4.53.58 PM.png").similar(0.90),
        '1': Pattern("Screen Shot 2017-02-09 at 5.23.40 PM.png").similar(0.90),
        '2': Pattern("Screen Shot 2017-02-09 at 5.28.10 PM.png").similar(0.90),
        '3': Pattern("Screen Shot 2017-02-09 at 5.28.15 PM.png").similar(0.90),
        '4': Pattern("Screen Shot 2017-02-09 at 5.49.16 PM.png").similar(0.90),
        '5': Pattern("Screen Shot 2017-02-09 at 5.50.30 PM.png").similar(0.90),
        '6': Pattern("Screen Shot 2017-02-09 at 5.52.50 PM.png").similar(0.90),
        '7': Pattern("Screen Shot 2017-02-09 at 5.55.42 PM.png").similar(0.90)}
x = int(happy_face.getX()-448)
y = int(happy_face.getY()+30)
box_size = 30
box_w = 30
box_h = 16
w = box_w*box_size
h = box_h*box_size

def match(region, pattern):
    try:
        return region.findAll(pattern)
    except FindFailed:
        return []

has_move = True
Settings.MoveMouseDelay = 0
# split the board into segments
h0 = box_h//2*box_size
board_regions = [Region(x, y, w, h0), Region(x, y+h0, w, h-h0)]
def my_click(positions):
    for i in xrange(2):
        for r,c in positions:
            click(Location(x+c*30+15, y+r*30+15))

while has_move:
    board = ("_"*30+"\n")*16
    print 'Analyzing patterns..'
    for k, pattern in box_patterns.iteritems():
        for region in board_regions:
            for m in match(region, pattern):
                x0 = (m.getX()-x)//30
                y0 = (m.getY()-y)//30
                i = int(y0*31+x0)
                board = board[:i] + k + board[i+1:]
    print board

    solver = Solver.from_string(board, 30, 16)
    solver.solve()
    print solver.to_string()
    print 'solved numbers: %s, solved bombs: %s' % (len(solver.revealed_numbers), len(solver.revealed_bombs))
    if len(solver.revealed_numbers) == 0:
        print '%s chance of kaboom at %s' % (solver.guess_prob, solver.guess_pos)
        my_click([solver.guess_pos])
    else:
        my_click(solver.revealed_numbers)

    has_move = exists("Screen Shot 2017-02-09 at 4.11.06 PM.png")
    hover(happy_face)
