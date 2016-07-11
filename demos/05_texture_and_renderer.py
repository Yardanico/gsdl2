import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption("05_texture_and_renderer.py - im in ur hardwarez")
screen_rect = screen.get_rect()
renderer = gsdl2.display.get_renderer()
clock = gsdl2.Clock()
fps = 33

block = gsdl2.image.load('tomato.png')
block_rect = block.get_rect(center=screen_rect.center)

block_texture = gsdl2.texture.Texture(renderer, block)

running = True

while running:
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                running = False

    renderer.clear()
    renderer.copy(block_texture, block_rect)
    renderer.present()
