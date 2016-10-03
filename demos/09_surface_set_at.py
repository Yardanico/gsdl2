import gsdl2
from gsdl2.locals import Color, QUIT, KEYDOWN, S_ESCAPE

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('09_surface_set_at.py - Setting pixels to red')
clock = gsdl2.Clock()
fps = 60

red = gsdl2.color.THECOLORS["red"]

for i in range(400):
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                quit()
    screen.set_at((i, i), red)
    screen.set_at((i - 15, i - 15), red)
    gsdl2.display.flip()
