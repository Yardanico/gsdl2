import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE


gsdl2.init()
gsdl2.mixer.init()

screen = gsdl2.display.set_mode((400, 50))
gsdl2.display.set_caption("07_mixer.py - It's a many-key one-note piano")
clock = gsdl2.Clock()
fps = 4

sound = gsdl2.mixer.Sound('1.ogg')
channel = None

running = True

while running:
    clock.tick(fps)

    for e in gsdl2.event.get():
        if e.type == QUIT:
            running = False
        if e.type == KEYDOWN:
            if e.scancode == S_ESCAPE:
                running = False
            else:
                sound.play()
