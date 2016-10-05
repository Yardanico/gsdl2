import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption("04_blit_scaled.py - It's...tomater?")
clock = gsdl2.Clock()
fps = 60
block = gsdl2.image.load('tomato.png')
block_rect = block.get_rect()
scale_rect = block.get_rect()
stretch_x = 1
stretch_y = 1
sdx = 2
sdy = 1
move_x = 1
move_y = 2
mdx = 2
mdy = 1

running = True

while running:
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                running = False

    move_x += mdx
    if not (0 < move_x < 500):
        mdx *= -1
    move_y += mdy
    if not (0 < move_y < 400):
        mdy *= -1
    scale_rect.topleft = move_x, move_y

    stretch_x += sdx
    if not (0 < stretch_x < 100):
        sdx *= -1
    stretch_y += sdy
    if not (0 < stretch_y < 100):
        sdy *= -1
    scale_rect.size = block_rect.w + stretch_x, block_rect.h + stretch_y

    screen.fill((0, 0, 0))
    scaled_block = gsdl2.transform.scale(block, scale_rect.get_size())
    screen.blit(scaled_block, scale_rect)
    # screen.blit_scaled(block, scale_rect, block_rect)
    gsdl2.display.flip()
