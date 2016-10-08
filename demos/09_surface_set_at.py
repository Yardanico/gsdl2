import gsdl2
from gsdl2.locals import *

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('09_surface_set_at.py - Use mouse to set pixels')
clock = gsdl2.Clock()
fps = 60

orange = gsdl2.color.THECOLORS['orangered']
cyan = gsdl2.color.THECOLORS['cyan']
green = gsdl2.color.THECOLORS['limegreen']
yellow = gsdl2.color.THECOLORS['yellow']

count = 5  # pixels count

while True:
    clock.tick(60)  # we don't want to waste CPU clock
    state = gsdl2.mouse.get_pressed()  # get mouse buttons state (lmb, mmb, rmb)
    if state[0]:  # if left button pressed
        x, y = gsdl2.mouse.get_pos()  # get mouse coords
        for x_cord in range(count):
            for y_cord in range(count):
                # Windows logo (don't blame me for this)
                screen.set_at((x + x_cord, y + y_cord), yellow)  # right lower
                screen.set_at((x - x_cord, y - y_cord), orange)  # left upper
                screen.set_at((x + x_cord, y - y_cord), green)  # right upper
                screen.set_at((x - x_cord, y + y_cord), cyan)  # left lower
    for e in gsdl2.event.get():
        if e.type == MOUSEWHEEL:
            if e.pos[1]:  # if wheel up
                # make drawing bigger amount of pixels
                count += 1
            elif e.pos[2]:  # if wheel down
                # smaller amount of pixels
                count -= 1

        elif e.type == QUIT:
            quit()

        elif e.type == KEYDOWN:
            if e.scancode == S_R:  # reset surface
                screen.fill((0, 0, 0))
            if e.scancode == S_ESCAPE:
                quit()

    gsdl2.display.flip()
