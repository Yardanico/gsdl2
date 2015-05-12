import gsdl2

gsdl2.init()

screen = gsdl2.display.set_mode((640, 480))
gsdl2.display.set_caption('01_surface.py - Using a surface (window will close in 4 seconds)')
clock = gsdl2.Clock()
fps = 100

block = gsdl2.surface.Surface((128, 128))
block.fill((255, 0, 0))
block_rect = block.get_rect()

for i in range(400):
    clock.tick(fps)

    block_rect.topleft = i, i

    screen.fill((0, 0, 0))
    screen.blit(block, block_rect)
    gsdl2.display.flip()
