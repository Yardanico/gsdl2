"""80_megaballs.py - many, many moving rects

Usage: python 80_megaballs.py [num_balls]

Experiment or see NUM_BALLS NOTE for a comment on choosing num_balls.
"""

import random
import sys

try:
    import gsdl2
except ImportError:
    # Stupid Windows and Cygwin
    sys.path.append('.')
    sys.path.append('..')
    import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE, S_SPACE


print('Python: {}'.format(sys.executable))

try:
    NUM_BALLS = int(sys.argv[1])
except ValueError:
    print('usage: python 01_transform.py [num_balls]')
    sys.exit(0)
except IndexError:
    #=================================================================
    #  NUM_BALLS NOTE:
    #
    #  pypy on an i5 or i7 with a decent gfx card renders (HW) 20,000
    #  @ 70 fps. Software blit handles about 20,000 @ 60 fps.
    #
    #  CPython on the same platform handles about 2,000 balls in HW.
    #  SW struggles with 2,000 looking a bit choppy.
    #=================================================================
    if 'pypy' in sys.executable:
        NUM_BALLS = 20000
    else:
        NUM_BALLS = 2000


class Ball(object):

    surface = None
    texture = None

    def __init__(self, x, y, color):
        object.__init__(self)

        self.rect = gsdl2.Rect(x, y, 8, 8)

        if self.surface is None:
            Ball.surface = gsdl2.Surface(self.rect.size)
            Ball.surface.fill(color)
            Ball.texture = gsdl2.Texture(gsdl2.display.get_renderer(), Ball.surface)

        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])

    def update(self, screen_rect):
        rect = self.rect

        rect.x += self.dx
        rect.y += self.dy

        if rect.x < 0:
            rect.x = 0
            self.dx *= -1
        elif rect.right > screen_rect.right:
            rect.right = screen_rect.right
            self.dx *= -1

        if rect.y < 0:
            rect.y = 0
            self.dy *= -1
        elif rect.bottom > screen_rect.bottom:
            rect.bottom = screen_rect.bottom
            self.dy *= -1


class Game(object):

    def __init__(self, resolution=(1024, 768)):
        self.screen = gsdl2.display.set_mode(resolution)
        self.screen_rect = self.screen.get_rect()
        self.renderer = gsdl2.display.get_renderer()
        self.renderer.set_draw_color((96, 0, 96, 0))
        self.fill_color = 0, 0, 96, 0

        self.clock = gsdl2.Clock()
        self.elapsed = 0.0

        self.balls = []
        for i in range(NUM_BALLS):
            self.balls.append(Ball(random.randrange(resolution[0]), random.randrange(resolution[1]), (0xff, 0xff, 0)))

        self.use_renderer = False
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            ms = self.clock.tick()
            dt = ms / 1000.0
            self.update(dt)

    def update(self, dt):
        self.update_caption(dt)
        self.update_balls()
        self.update_events()
        self.draw()

    def update_caption(self, dt):
        self.elapsed += dt
        if self.elapsed >= 1.0:
            gsdl2.display.set_caption('{} fps | Balls: {} | Screen: {}x{} | Renderer: {}'.format(
                int(self.clock.get_fps()), NUM_BALLS, self.screen_rect.w, self.screen_rect.h, self.use_renderer))
            self.elapsed -= 1.0

    def update_balls(self):
        screen_rect = self.screen_rect
        for ball in self.balls:
            ball.update(screen_rect)

    def update_events(self):
        for e in gsdl2.event.get():
            if e.type == KEYDOWN:
                if e.scancode == S_SPACE:
                    self.use_renderer = not self.use_renderer
                elif e.scancode == S_ESCAPE:
                    self.running = False
            elif e.type == QUIT:
                self.running = False

    def draw(self):
        if self.use_renderer:
            self.render_balls()
        else:
            self.blit_balls()

    def blit_balls(self):
        screen = self.screen
        blit = screen.blit
        screen.fill(self.fill_color)
        for ball in self.balls:
            blit(ball.surface, ball.rect)
        gsdl2.display.flip()

    def render_balls(self):
        renderer = self.renderer
        copy = renderer.copy
        renderer.clear()
        for ball in self.balls:
            copy(ball.texture, ball.rect)
        renderer.present()


if __name__ == '__main__':
    gsdl2.init()
    game = Game()
    game.run()
