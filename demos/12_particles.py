import random

import gsdl2
from gsdl2.locals import QUIT, KEYDOWN, S_ESCAPE, S_TAB, MOUSEMOTION


SCALE = 3.0
SPARKS_PER_SECOND = 640
MAX_PARTICLES = 2000


class Spark(gsdl2.particles.Particle):

    image = None

    def __init__(self, x, y, life, vx, vy):
        gsdl2.particles.Particle.__init__(self, x, y, life)
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.alpha = 255
        self.lifespan = life

        if self.image is None:
            surf = gsdl2.Surface((2, 2))
            surf.fill(gsdl2.Color(240, 248, 255))
            self.image = gsdl2.Texture(gsdl2.display.get_renderer(), surf)
            self.image.set_blendmode(gsdl2.sdl_lib.SDL_BLENDMODE_BLEND)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, dt, world):
        self.alpha = abs(int(255 * self.life / self.lifespan))

        scale = SCALE
        vx = self.vx
        vy = self.vy
        vx -= vx * 1.0/4.0 * dt * scale
        vy += 9.8 * dt * scale
        self.vx = vx
        self.vy = vy

        self.x += vx * dt * scale
        self.y += vy * dt * scale

        self.rect.center = self.x, self.y


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
        self.elapsed -= dt
        while self.elapsed <= 0.0:
            self.elapsed += self.rate
            if len(self.particles) >= self.max_particles:
                continue
            p = Spark(self.x, self.y,
                      random.randrange(1, 2) * SCALE,
                      (random.random() * 16 - 8) * SCALE,
                      (random.random() * 16 - 8) * SCALE)
            self.particles.append(p)
            if self.debug_particle is None:
                self.debug_particle = p

    @staticmethod
    def _update(dt, world, livingones):
        for p in livingones:
            p.update(dt, world)

    def _delete(self, dt, world, deadones):
        remove = self.particles.remove
        for p in deadones:
            remove(p)
            if p is self.debug_particle:
                self.debug_particle = None

    def update(self, dt, mousex, mousey):
        self.x = mousex
        self.y = mousey
        self.particles_engine.process(dt, None, self.particles)

    def render(self, renderer):
        for p in self.particles:
            p.image.set_alpha(p.alpha)
            renderer.copy(p.image, p.rect)


class Game(object):
    def __init__(self):
        self.screen = gsdl2.display.set_mode((640, 480))
        gsdl2.display.set_caption("12_particles.py - ")
        self.screen_rect = self.screen.get_rect()
        self.renderer = gsdl2.display.get_window().create_renderer()
        self.clock = gsdl2.time.FixedDriver(self.update, 1.0 / 15.0)
        self.which_fps = [30, 60, 120, 240, 360, 15]
        self.fps = 15
        self.elapsed = 1.0
        self.clock.new_schedule(self.caption, 1.0)

        self.mousex, self.mousey = self.screen_rect.center
        self.sparkler = Sparkler(
            self.mousex, self.mousey, sparks_per_second=SPARKS_PER_SECOND, max_particles=MAX_PARTICLES)

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick()

    def update(self, dt):
        self.elapsed -= dt
        for e in gsdl2.event.get():
            if e.type == QUIT:
                self.running = False
            elif e.type == KEYDOWN:
                if e.scancode == S_ESCAPE:
                    self.running = False
                elif e.scancode == S_TAB:
                    self.fps = self.which_fps.pop(0)
                    self.which_fps.append(self.fps)
                    self.clock.change_master(1.0 / self.fps, schedules_too=True)
            elif e.type == MOUSEMOTION:
                self.mousex, self.mousey = e.pos

        self.sparkler.update(dt, self.mousex, self.mousey)

        self.renderer.clear()
        self.sparkler.render(self.renderer)
        self.renderer.present()

    def caption(self, sched):
        if self.elapsed <= 0.0:
            self.elapsed += 1.0
            gsdl2.display.set_caption(
                'FPS: real={real} target={target} | Dt: {dt:0.3f} | Particles: {particles}'.format(
                    real=int(self.clock.per_second()),
                    target=self.fps,
                    dt=self.clock.period,
                    particles=len(self.sparkler.particles)))


def main():
    gsdl2.init()
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
