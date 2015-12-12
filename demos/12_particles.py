"""12_particles.py - particle demo using textures, and the first robust test of FixedDriver

Usage:
    python 12_particles.py [scale=float] [sparks_per_second=int] [max_particles=int] [profile]

Based on ParticleEngine by marcusva in py-sdl2:
https://bitbucket.org/marcusva/py-sdl2
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

import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE, S_TAB, S_I, MOUSEMOTION


print('Python: {}'.format(sys.executable))

if 'pypy' in sys.executable:
    CONFIG = dict(
        scale=3.0,              # pixels per unit
        sparks_per_second=640,  # max sparks released per tick
        max_particles=2000,     # max sparks alive at any time
        profile=False,
    )
else:
    CONFIG = dict(
        scale=3.0,              # pixels per unit
        sparks_per_second=320,  # max sparks released per tick
        max_particles=1000,     # max sparks alive at any time
        profile=False,
    )



def parse_args():
    if 'profile' in sys.argv:
        CONFIG['profile'] = True
        sys.argv.remove('profile')
    try:
        for arg in sys.argv[1:]:
            key, value = arg.split('=')
            assert key in CONFIG
            if key == 'scale':
                CONFIG[key] = float(value)
            elif key in ('sparks_per_second', 'max_particles'):
                CONFIG[key] = int(value)
    except ValueError:
        print('usage: python 12_particles.py [scale=float] [sparks_per_second=int] [max_particles=int] [profile]')
        sys.exit(1)


class Spark(gsdl2.particles.Particle):

    image = None

    def __init__(self, x, y, life, vx, vy):
        gsdl2.particles.Particle.__init__(self, x, y, life)
        self.vx = vx
        self.vy = vy
        self.alpha = 255
        self.lifespan = life
        self.oldx = x
        self.oldy = y

        if self.image is None:
            surf = gsdl2.Surface((2, 2))
            surf.fill(gsdl2.Color(240, 248, 255))
            self.image = gsdl2.Texture(gsdl2.display.get_renderer(), surf)
            self.image.set_blendmode(gsdl2.sdl_lib.SDL_BLENDMODE_BLEND)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt, world):
        """just yer basic time-and-space-scaled acceleration"""
        self.alpha = abs(int(255 * self.life / self.lifespan))

        self.oldx = self.x
        self.oldy = self.y

        scale = CONFIG['scale']
        vx = self.vx
        vy = self.vy
        vx -= vx * 1.0/4.0 * dt * scale
        vy += 9.8 * dt * scale
        self.vx = vx
        self.vy = vy

        self.x += vx * dt * scale
        self.y += vy * dt * scale

        self.rect.center = self.x, self.y

    def get_rect_interpolated(self, interp):
        """interpolate between the old and current position"""
        x0 = self.oldx
        x1 = self.x
        y0 = self.oldy
        y1 = self.y
        rect = self.rect
        rect.topleft = int(x0 + (x1 - x0) * interp), int(y0 + (y1 - y0) * interp)
        return rect


class Sparkler(object):

    def __init__(self, x, y, sparks_per_second=100, max_particles=250):
        self.particles_engine = gsdl2.particles.ParticleEngine()
        self.particles = []
        self.x = x
        self.y = y
        self.rate = 1.0 / sparks_per_second
        self.elapsed = 0.0
        self.max_particles = max_particles

        self.particles_engine.createfunc = self._create
        self.particles_engine.updatefunc = self._update
        self.particles_engine.deletefunc = self._delete

        self.debug_particle = None

    def _create(self, dt, world, components):
        """pluggable spark generator"""
        self.elapsed -= dt
        scale = CONFIG['scale']
        while self.elapsed <= 0.0:
            self.elapsed += self.rate
            if len(self.particles) >= self.max_particles:
                continue
            p = Spark(self.x, self.y,
                      random.randrange(1, 2) * scale,
                      (random.random() * 16 - 8) * scale,
                      (random.random() * 16 - 8) * scale)
            self.particles.append(p)
            if self.debug_particle is None:
                self.debug_particle = p

    @staticmethod
    def _update(dt, world, livingones):
        """pluggable live spark updater"""
        for p in livingones:
            p.update(dt, world)

    def _delete(self, dt, world, deadones):
        """pluggable dead spark remover"""
        remove = self.particles.remove
        for p in deadones:
            remove(p)
            if p is self.debug_particle:
                self.debug_particle = None

    def update(self, dt, mousex, mousey):
        """update model"""
        self.x = mousex
        self.y = mousey
        self.particles_engine.process(dt, None, self.particles)

    def render(self, renderer):
        """basic pygame-like renderer"""
        for p in self.particles:
            p.image.set_alpha(p.alpha)
            renderer.copy(p.image, p.rect)

    def render_interpolated(self, renderer, interp):
        """interpolated renderer"""
        for p in self.particles:
            p.image.set_alpha(p.alpha)
            renderer.copy(p.image, p.get_rect_interpolated(interp))


class Game(object):
    def __init__(self):
        self.screen = gsdl2.display.set_mode((640, 480))
        gsdl2.display.set_caption("12_particles.py - Oooh sparklies")
        self.screen_rect = self.screen.get_rect()
        self.renderer = gsdl2.display.get_renderer()

        # switchable model pulse rate, clock, and schedules
        self.which_interval = [30, 60, 120, 240, 360, 15]
        self.clock = gsdl2.time.FixedDriver(self.update, 1.0 / 15.0)
        self.clock.new_schedule(self.caption, 1.0)
        self.renderer_schedule = self.clock.new_schedule(self.draw, 0.0, keep_history=True)

        # on/off interpolation
        self.do_interpolation = True

        # sparkler follows mouse location
        self.mousex, self.mousey = self.screen_rect.center
        self.sparkler = Sparkler(self.mousex, self.mousey,
                                 sparks_per_second=CONFIG['sparks_per_second'], max_particles=CONFIG['max_particles'])

    def run(self):
        """just a busy loop that turns the clock"""
        self.running = True

        while self.running:
            self.clock.tick()

    def update(self, dt):
        """master callback"""
        self.handle_events()
        self.sparkler.update(dt, self.mousex, self.mousey)

        # Interpolation can be toggled on/off. This is done by enabling/disabling self.renderer_schedule, because if it
        # is off there is no point in spamming self.draw. In this case we want self.update and self.draw to be in
        # lockstep, so we need to call self.draw from self.update. This is nicer than running separate update and draw
        # schedules that are not in lockstep: we would often get two updates in a row and two draws in a row and it
        # would look very jerky.
        if not self.do_interpolation:
            self.draw(None)

    def handle_events(self):
        for e in gsdl2.event.get():
            if e.type == QUIT:
                self.running = False
            elif e.type == KEYDOWN:
                if e.scancode == S_ESCAPE:
                    self.running = False
                elif e.scancode == S_TAB:
                    # Advance ticks per second setting
                    per_second = self.which_interval.pop(0)
                    self.which_interval.append(per_second)
                    self.clock.change(1.0 / per_second)
                elif e.scancode == S_I:
                    # Toggle interpolation
                    self.do_interpolation = not self.do_interpolation
                    if self.do_interpolation:
                        self.renderer_schedule.set_running(True)
                    else:
                        self.renderer_schedule.set_running(False)
            elif e.type == MOUSEMOTION:
                self.mousex, self.mousey = e.pos

    def draw(self, sched):
        """renderer callback"""
        self.renderer.clear()
        if self.do_interpolation:
            interp = sched.interp
            self.sparkler.render_interpolated(self.renderer, interp)
        else:
            self.sparkler.render(self.renderer)
        self.renderer.present()

    def caption(self, sched):
        """window caption callback"""
        dt = self.clock.period
        target = 1.0 / dt
        gsdl2.display.set_caption(
            'Master: real={real}/s target={target}/s | FPS: {fps}/s | Particles: {particles} | Interp: {interp}'.format(
                real=int(self.clock.per_second()),
                target=int(target),
                fps=int(self.renderer_schedule.per_second()),
                particles=len(self.sparkler.particles),
                interp=self.do_interpolation))


def main():
    gsdl2.init()
    game = Game()
    game.run()


if __name__ == '__main__':
    parse_args()
    gsdl2.init()
    if CONFIG['profile']:
        cProfile.run('main()', 'prof.dat')
        p = pstats.Stats('prof.dat')
        p.sort_stats('time').print_stats()
    else:
        main()
