"""81_transform.py - rotation exercise

Usage: python 81_transform.py [profile] [num_balls]

Note: There is no rotate function in SDL2 for software (surfaces).

Note: blit_balls() demontrates the use of SDL_BlitScaled(). In practice, and as with pygame, caching the transformed
surfaces would be a lot more efficient. However for the texture renderer this is unnecessary.
"""

import cProfile
import pstats
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

PROFILE = False
if 'profile' in sys.argv:
    PROFILE = True
    sys.argv.remove('profile')
try:
    NUM_BALLS = int(sys.argv[1])
except ValueError:
    print('usage: python 01_transform.py [profile] [num_balls]')
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

        self.use_renderer = True
        self.running = False
        self.rotation_msg = {True: 'Go go go!', False: 'Ach, software... no rotation for j00!'}

        self.all_balls = []
        for i in range(NUM_BALLS):
            self.all_balls.append(Ball())
        self.src_rect = gsdl2.Rect(0, 0, *Ball.texture.get_size())
        self._render_balls = self.all_balls[:]
        self._blit_balls = self.all_balls[:NUM_BALLS // 4]
        self.balls = self._render_balls if self.use_renderer else self._blit_balls

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
                int(self.clock.get_fps()), len(self.balls),
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
                    self.balls = self._render_balls if self.use_renderer else self._blit_balls
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
        for ball in self.balls:
            # TODO: software rotate here
            scale = ball.scale
            r = ball.rect.scale(scale, scale)
            self.screen.blit_scaled(ball.surface, r)
        gsdl2.display.flip()

    def render_balls(self):
        renderer = self.renderer
        renderer.clear()
        src_rect = self.src_rect
        copy_ex = renderer.copy_ex
        for ball in self.balls:
            dst_rect = ball.rect
            angle = ball.angle
            scale = ball.scale
            copy_ex(ball.texture, dst_rect.scale(scale, scale), src_rect, angle, None, False)
        renderer.present()


def main():
    try:
        game = Game()
        game.run()
    except:
        pass
    finally:
        gsdl2.quit()


if __name__ == '__main__':
    gsdl2.init()
    if PROFILE:
        cProfile.run('main()', 'prof.dat')
        p = pstats.Stats('prof.dat')
        p.sort_stats('time').print_stats()
    else:
        main()
