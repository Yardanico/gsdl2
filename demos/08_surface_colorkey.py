import gsdl2
from gsdl2.locals import Color, Rect, QUIT, KEYDOWN, S_ESCAPE


gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('08_surface_colorkey.py - Colorkey transparency')
clock = gsdl2.Clock()
fps = 100

white = Color(255, 255, 255)
red = Color(255, 0, 0)
green = Color(0, 255, 0)
blue = Color(0, 0, 255)
purple = Color(255, 0, 255)

# some colored squares for backround variation
i = 128
blocks = []
for c in red, green, blue:
    block = gsdl2.surface.Surface((128, 128))
    block.fill(c)
    block_rect = block.get_rect(topleft=(i, i))
    blocks.append((block, block_rect))
    i += 128

# a square with concentric rings using a colorkey
ball = gsdl2.surface.Surface((128, 128))
ball_rect = ball.get_rect()
ball.fill(purple)
ball.fill(white, ball_rect.scale(0.75, 0.75))
ball.fill(purple, ball_rect.scale(0.5, 0.5))
ball.fill(white, ball_rect.scale(0.25, 0.25))
ball.fill(purple, ball_rect.scale(0.1, 0.1))
ball.set_colorkey(white)

for i in range(400):
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                running = False

    screen.fill((0, 0, 0))
    for block, block_rect in blocks:
        screen.blit(block, block_rect)
    ball_rect.topleft = i, i
    screen.blit(ball, ball_rect)
    gsdl2.display.flip()
