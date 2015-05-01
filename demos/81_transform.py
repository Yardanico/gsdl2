"""01_transform.py - rotation exercise

Usage: python 01_transform.py [num_balls]

Note: There is no rotate function in SDL2 for software (surfaces).
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
from gsdl2 import sdlpixels
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE, S_SPACE, S_RETURN


print('Python: {}'.format(sys.executable))

try:
    NUM_BALLS = int(sys.argv[1])
except ValueError:
    print('usage: python 01_transform.py [num_balls]')
    sys.exit(0)
except IndexError:
    if 'pypy' in sys.executable:
        NUM_BALLS = 1000
    else:
        NUM_BALLS = 750


# Step through these with K_RETURN if you want to try different surface formats.
# These only affect blit performance. No effect on texture rendering.
formats = [
    sdlpixels.SDL_PIXELFORMAT_INDEX1LSB,
    sdlpixels.SDL_PIXELFORMAT_INDEX1MSB,
    sdlpixels.SDL_PIXELFORMAT_INDEX4LSB,
    sdlpixels.SDL_PIXELFORMAT_INDEX4MSB,
    sdlpixels.SDL_PIXELFORMAT_INDEX8,
    sdlpixels.SDL_PIXELFORMAT_RGB332,
    sdlpixels.SDL_PIXELFORMAT_RGB444,
    sdlpixels.SDL_PIXELFORMAT_RGB555,
    sdlpixels.SDL_PIXELFORMAT_BGR555,
    sdlpixels.SDL_PIXELFORMAT_ARGB4444,
    sdlpixels.SDL_PIXELFORMAT_RGBA4444,
    sdlpixels.SDL_PIXELFORMAT_ABGR4444,
    sdlpixels.SDL_PIXELFORMAT_BGRA4444,
    sdlpixels.SDL_PIXELFORMAT_ARGB1555,
    sdlpixels.SDL_PIXELFORMAT_RGBA5551,
    sdlpixels.SDL_PIXELFORMAT_ABGR1555,
    sdlpixels.SDL_PIXELFORMAT_BGRA5551,
    sdlpixels.SDL_PIXELFORMAT_RGB565,
    sdlpixels.SDL_PIXELFORMAT_BGR565,
    sdlpixels.SDL_PIXELFORMAT_RGB24,
    sdlpixels.SDL_PIXELFORMAT_BGR24,
    sdlpixels.SDL_PIXELFORMAT_RGB888,
    sdlpixels.SDL_PIXELFORMAT_RGBX8888,
    sdlpixels.SDL_PIXELFORMAT_BGR888,
    sdlpixels.SDL_PIXELFORMAT_BGRX8888,
    sdlpixels.SDL_PIXELFORMAT_ARGB8888,
    sdlpixels.SDL_PIXELFORMAT_RGBA8888,
    sdlpixels.SDL_PIXELFORMAT_ABGR8888,
    sdlpixels.SDL_PIXELFORMAT_BGRA8888,
    # The following are esoteric and probably will cause an sdlpixels2 crash.
    # sdlpixels.SDL_PIXELFORMAT_ARGB2101010,
    # sdlpixels.SDL_PIXELFORMAT_YV12,
    # sdlpixels.SDL_PIXELFORMAT_IYUV,
    # sdlpixels.SDL_PIXELFORMAT_YUY2,
    # sdlpixels.SDL_PIXELFORMAT_UYVY,
    # sdlpixels.SDL_PIXELFORMAT_YVYU,
]
last_format = formats[-1]


class Ball(object):

    orig_surface = None
    surface = None
    texture = None

    def __init__(self):
        object.__init__(self)

        if self.surface is None:
            Ball.orig_surface = gsdl2.image.load('tomato.png')
            Ball.surface = Ball.orig_surface.convert_alpha()
            Ball.texture = gsdl2.Texture(gsdl2.display.get_renderer(), Ball.surface)

        self.rect = self.surface.get_rect()

        self.rect.x = random.randrange(0, 900)
        self.rect.y = random.randrange(0, 700)

        self.angle = random.randrange(360)
        self.spin = random.uniform(1.0, 5.0)
        self.spin *= random.choice((-1.0, 1.0))

        self.scale = 1.0
        self.grow_rate = random.uniform(0.005, 0.01)
        self.grow_rate *= random.choice((-1.0, 1.0))
        self.scale_min = 0.8
        self.scale_max = 1.2

    def update(self):
        self.angle += self.spin
        self.angle %= 360.0

        self.scale += self.grow_rate
        if self.scale_min > self.scale or self.scale_max < self.scale:
            self.grow_rate *= -1.0


class Game(object):

    def __init__(self, resolution=(1024, 768)):
        self.screen = gsdl2.display.set_mode(resolution)
        self.screen_rect = self.screen.get_rect()
        self.renderer = gsdl2.display.get_renderer()
        self.renderer.set_draw_color((96, 0, 96, 0))
        self.fill_color = (0, 0, 96, 0)

        self.clock = gsdl2.Clock()
        self.elapsed = 0.0

        self.balls = []
        for i in range(NUM_BALLS):
            self.balls.append(Ball())

        self.use_renderer = True
        self.running = False
        self.rotation_msg = {True: 'Go go go!', False: 'Ach, software... no rotation for j00!'}

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
            gsdl2.display.set_caption('{} fps | Balls: {} | Screen: {}x{} | Renderer: {} | Rotation: {}'.format(
                int(self.clock.get_fps()), NUM_BALLS if self.use_renderer else NUM_BALLS / 3,
                self.screen_rect.w, self.screen_rect.h, self.use_renderer, self.rotation_msg[self.use_renderer]))
            self.elapsed -= 1.0

    def update_balls(self):
        for ball in self.balls:
            ball.update()

    def update_events(self):
        for e in gsdl2.event.get():
            if e.type == KEYDOWN:
                if e.scancode == S_SPACE:
                    self.use_renderer = not self.use_renderer
                elif e.scancode == S_ESCAPE:
                    self.running = False
                elif e.scancode == S_RETURN:
                    fmt = formats.pop(0)
                    formats.append(fmt)
                    print('new format={}'.format(sdlpixels.pixel_format_name(fmt)))
                    Ball.surface = Ball.orig_surface.convert_alpha(fmt)
                    if fmt == last_format:
                        print('==== end of formats reached ====')
            elif e.type == QUIT:
                self.running = False

    def draw(self):
        if self.use_renderer:
            self.render_balls()
        else:
            self.blit_balls()

    def blit_balls(self):
        self.screen.fill(self.fill_color)
        for ball in self.balls[:NUM_BALLS / 3]:
            # TODO: software rotate here
            scale = ball.scale
            self.screen.blit_scaled(ball.surface, ball.rect.scale(scale, scale))
        gsdl2.display.flip()

    def render_balls(self):
        self.renderer.clear()
        for ball in self.balls:
            w, h = ball.rect.size
            angle = ball.angle
            scale = ball.scale
            self.renderer.copy_ex(ball.texture, ball.rect.scale(scale, scale), (0, 0, w, h), angle, None, False)
        self.renderer.present()


def main():
    try:
        gsdl2.init()
        game = Game()
        game.run()
    except:
        pass
    finally:
        gsdl2.quit()


if __name__ == '__main__':
    main()
