from solver import Solver
import time
location = find("Screen Shot 2017-02-09 at 4.11.06 PM.png").getTarget()
box_patterns = {
        '0': Pattern("Screen Shot 2017-02-09 at 4.53.58 PM.png").similar(0.90),
        '1': Pattern("Screen Shot 2017-02-09 at 5.23.40 PM.png").similar(0.90),
        '2': Pattern("Screen Shot 2017-02-09 at 5.28.10 PM.png").similar(0.90),
        '3': Pattern("Screen Shot 2017-02-09 at 5.28.15 PM.png").similar(0.90),
        '4': Pattern("Screen Shot 2017-02-09 at 5.49.16 PM.png").similar(0.90),
        '5': Pattern("Screen Shot 2017-02-09 at 5.50.30 PM.png").similar(0.90),
        '6': Pattern("Screen Shot 2017-02-09 at 5.52.50 PM.png").similar(0.90),
        '7': Pattern("Screen Shot 2017-02-09 at 5.55.42 PM.png").similar(0.90)}
x = int(location.getX()-448)
y = int(location.getY()+30)
box_size = 30
w = 30*box_size
h = 16*box_size

def match(region, pattern):
    try:
        return region.findAll(pattern)
    except FindFailed:
        return []

has_move = True
Settings.MoveMouseDelay = 0
# might need to separate the region due to too many matches
board_region = Region(x, y, w, h)
while has_move:
    board = ("_"*30+"\n")*16
    print 'Analyzing patterns..'
    for k, pattern in box_patterns.iteritems():
        for m in match(board_region, pattern):
            x0 = (m.getX()-x)//30
            y0 = (m.getY()-y)//30
            i = int(y0*31+x0)
            board = board[:i] + k + board[i+1:]
    print board

    solver = Solver.from_string(board, 30, 16)
    solver.solve()
    print solver.revealed_numbers
    for r,c in solver.revealed_numbers:
        loc = Location(x+c*30+15, y+r*30+15)
        click(loc)
    has_move = len(solver.revealed_numbers) > 0
    hover(location)
