import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption("03_image.py - It's a french fried tomater")
clock = gsdl2.Clock()
fps = 60

block = gsdl2.image.load('tomato.png')
block_rect = block.get_rect()

running = True

while running:
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    screen.blit(block, block_rect)
    gsdl2.display.flip()
