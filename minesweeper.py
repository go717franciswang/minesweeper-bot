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
setting = {
        'beginner': {
            'x': int(happy_face.getX()-135),
            'y': int(happy_face.getY()+30),
            'box_w': 9,
            'box_h': 9,
            'board_regions': [Region(int(happy_face.getX()-135), int(happy_face.getY()+30), 270, 270)]
            },
        'intermediate': {
            'x': int(happy_face.getX()-240),
            'y': int(happy_face.getY()+30),
            'box_w': 16,
            'box_h': 16,
            'board_regions': [Region(int(happy_face.getX()-240), int(happy_face.getY()+30), 480, 480)]
            },
        'advanced': {
            'x': int(happy_face.getX()-450),
            'y': int(happy_face.getY()+30),
            'box_w': 30,
            'box_h': 16,
            'board_regions': [
                Region(int(happy_face.getX()-450), int(happy_face.getY()+30), 450, 240),
                Region(int(happy_face.getX()-450), int(happy_face.getY()+30)+240, 450, 240)]
            }
        }
setting = setting['beginner']
box_size = 30

def match(region, pattern):
    try:
        return region.findAll(pattern)
    except FindFailed:
        return []

has_move = True
Settings.MoveMouseDelay = 0
# split the board into segments
h0 = setting['box_h']//2*box_size
def my_click(positions):
    for i in xrange(2):
        for r,c in positions:
            click(Location(setting['x']+(c+0.5)*box_size, setting['y']+(r+0.5)*box_size))

while has_move:
    board = ("_"*setting['box_w']+"\n")*setting['box_h']
    print 'Analyzing patterns..'
    for k, pattern in box_patterns.iteritems():
        for region in setting['board_regions']:
            for m in match(region, pattern):
                x0 = (m.getX()-setting['x'])//box_size
                y0 = (m.getY()-setting['y'])//box_size
                i = int(y0*(setting['box_w']+1)+x0)
                board = board[:i] + k + board[i+1:]
    print board

    solver = Solver.from_string(board, setting['box_w'], setting['box_h'])
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
