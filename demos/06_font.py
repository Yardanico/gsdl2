import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE, S_N, S_B, S_I, S_O, S_S, S_U


def set_caption():
    s = '06_font.py - N: {} | B: {} | I: {} | S: {} | U: {} | O: {}'.format(
        font.get_normal(), font.get_bold() > 0, font.get_italic() > 0, font.get_strikethrough() > 0,
                           font.get_underline() > 0, font.get_outline() > 0)
    gsdl2.display.set_caption(s)


def render_text(text):
    surf = font.render(text, fg_color)
    texture = gsdl2.texture.Texture(renderer, surf)
    rect = texture.get_rect(center=screen_rect.center)
    return texture, rect


gsdl2.init()

screen = gsdl2.display.set_mode((1024, 480))
screen_rect = screen.get_rect()
renderer = gsdl2.display.get_renderer()
clock = gsdl2.Clock()
fps = 33

font = gsdl2.Font('Vera.ttf', 48)
fg_color = gsdl2.Color(255, 0, 255)

font.set_outline(True)
font.set_underline(True)

set_caption()

words = 'ABCDEFG HIJKLMN OPQRST UVWXYZ'
word_texture, word_rect = render_text(words)

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
                if e.scancode == S_N:
                    font.set_normal()
                elif e.scancode == S_B:
                    font.set_bold(font.get_bold() == 0)
                elif e.scancode == S_I:
                    font.set_italic(font.get_italic() == 0)
                elif e.scancode == S_O:
                    font.set_outline(font.get_outline() == 0)
                elif e.scancode == S_S:
                    font.set_strikethrough(font.get_strikethrough() == 0)
                elif e.scancode == S_U:
                    font.set_underline(font.get_underline() == 0)
                word_texture, word_rect = render_text(words)
                set_caption()

    renderer.clear()
    renderer.copy(word_texture, word_rect)
    renderer.present()
