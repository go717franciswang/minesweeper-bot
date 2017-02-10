location = find("Screen Shot 2017-02-09 at 4.11.06 PM.png").getTarget()
box_patterns = {
        '0': Pattern("Screen Shot 2017-02-09 at 4.53.58 PM.png").exact(),
        '1': Pattern("Screen Shot 2017-02-09 at 5.23.40 PM.png").exact(),
        '2': Pattern("Screen Shot 2017-02-09 at 5.28.10 PM.png").exact(),
        '3': Pattern("Screen Shot 2017-02-09 at 5.28.15 PM.png").exact(),
        '4': Pattern("Screen Shot 2017-02-09 at 5.49.16 PM.png").exact(),
        '5': Pattern("Screen Shot 2017-02-09 at 5.50.30 PM.png").exact(),
        '6': Pattern("Screen Shot 2017-02-09 at 5.52.50 PM.png").exact(),
        '7': Pattern("Screen Shot 2017-02-09 at 5.55.42 PM.png").exact()}
x = location.getX()-448
y = location.getY()+30
box_size = 30
w = 30*box_size
h = 16*box_size

board = ""

def match(region, pattern):
    try:
        return region.findAll(pattern)
    except FindFailed:
        return []

board = ("_"*30+"\n")*16
r = Region(x, y, w, h)
for k, pattern in box_patterns.iteritems():
    for m in match(r, pattern):
        x0 = (m.getX()-x)//30
        y0 = (m.getY()-y)//30
        i = y0*31+x0
        board = board[:i] + k + board[i+1:]

print board
        
