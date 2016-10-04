import gsdl2
from gsdl2.locals import *

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('09_surface_set_at.py - Use mouse to set pixels')
clock = gsdl2.Clock()
fps = 60

red = gsdl2.color.THECOLORS["red"]

while True:
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                quit()
        elif e.type == MOUSEBUTTONDOWN:
            x,y = gsdl2.mouse.get_pos()
            for z in range(-5,5):
                screen.set_at((x+z,y), red)
                screen.set_at((x,y+z), red)
    gsdl2.display.flip()
