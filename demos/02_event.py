import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, KEYUP, S_ESCAPE

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('02_event.py - Use close-window button or Escape to exit')
clock = gsdl2.Clock()
fps = 33

block = gsdl2.surface.Surface((128, 128))
block.fill((255, 0, 0))
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
            else:
                print('KEYDOWN', e.key)
        elif e.type == KEYUP:
            print('KEYUP', e.key)
        else:
            print('unknown type', e.type)

    screen.fill((0, 0, 0))
    screen.blit(block, block_rect)
    gsdl2.display.flip()
