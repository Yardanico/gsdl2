"""82_scroll_pygame.py - scrolling tiles using pygame for performance comparison to 82_scroll.py

Usage: python 82_scroll_pygame.py [tilesize=WxH] [mapsize=WxH] [screen=WxH]

tilesize is the WxH of a tile in pixels
mapsize is the WxH of a map in tiles
screen is the window resolution

Defaults tuned for pypy:
    tilesize=16x16
    mapsize=200x200
    screen=1024x768

Recommended for CPython:
    tilesize=64x64

Example:
    python 82_scroll_pygame.py tilesize=64x64
"""

import random
import sys

try:
    import pygame
except ImportError:
    # Stupid Windows and Cygwin
    sys.path.append('.')
    sys.path.append('..')
    import pygame
from pygame.locals import Rect, Color, QUIT, KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN


CONFIG = dict(
    tilesize=(16, 16),
    mapsize=(100, 100),
    screen=(1024, 768),
)


def parse_args():
    """update CONFIG from sys.argv"""
    try:
        for arg in sys.argv[1:]:
            key, value = arg.split('=')
            assert key in CONFIG
            w, h = [int(s) for s in value.split('x')]
            assert w > 0 and h > 0
            CONFIG[key] = (w, h)
    except ValueError:
        print('usage: python 82_scroll.py [tilesize=WxH] [mapsize=WxH] [screen=WxH]')
        sys.exit(1)


class Sprite(object):

    def __init__(self, x, y, image):
        self.image = image
        self.rect = image.get_rect(topleft=(x, y))


class Game(object):

    # surfaces
    tile_images = []

    def __init__(self, resolution, tile_size, map_size):
        self.tile_size = tile_size
        self.map_size = map_size
        self.screen = pygame.display.set_mode(resolution)
        self.screen_rect = self.screen.get_rect()

        self.bgcolor = Color('black')

        # define the world as a rect; these are absolute coords
        mw, mh = map_size
        tw, th = tile_size
        self.world_rect = Rect(0, 0, tw * mw, th * mh)

        # load surfaces
        if not Game.tile_images:
            for color_name in 'green1', 'green2', 'green3', 'green4':
                color = Color(color_name)
                tile_image = pygame.Surface((tw, th))
                tile_image.fill(color)
                pygame.draw.rect(tile_image, Color('white'), Rect(0, 0, tw, th), 1)
                Game.tile_images.append(tile_image)

        # make the tile sprites
        self.tiles = []
        ww, wh = self.world_rect.size
        tw, th = self.tile_size
        for y in range(0, self.world_rect.h, th):
            for x in range(0, self.world_rect.w, tw):
                # darkest image for edge tiles
                if x == 0 or y == 0 or x == ww - tw or y == wh - th:
                    image = self.tile_images[-1]
                else:
                    image = random.choice(self.tile_images)
                sprite = Sprite(x, y, image)
                self.tiles.append(sprite)

        # scrolling movement
        self.scroll_speed = 5
        self.movex = 0
        self.movey = 0

        # these are used to manage culling and drawing
        self.visible_tiles = []
        self.scrap_rect = Rect(0, 0, tw, th)
        self.cam_rect = Rect(self.screen_rect)
        self.cam_pos_old = self.cam_rect.topleft
        # force visible tile selection
        self.cache_visible_tiles()

        # make the clock and schedule a couple timers
        self.clock = pygame.time.Clock()
        self.dt = 1.0 / 30.0
        self.update_timer = self.dt
        self.caption_timer = 1.0
        self.running = False

    def run(self):
        self.running = True
        while self.running:
            # step the timers
            ms = self.clock.tick()
            dt = ms / 1000.0
            self.update_timer -= dt
            self.caption_timer -= dt

            # update caption
            if self.update_timer <= 0.0:
                self.update(self.dt)
                self.update_timer += self.dt

            # calculate interpolation for draw()
            diff = self.dt - self.update_timer
            if diff <= 0.0:
                interp = 0.0
            else:
                interp = diff / self.dt
            if interp < 0.0:
                interp = 0.0
            elif interp > 1.0:
                interp = 1.0

            # draw game
            self.draw(interp)

            # update caption
            if self.caption_timer <= 0.0:
                self.update_caption(self.dt)
                self.caption_timer += 1.0

    def update(self, dt):
        """update the model - called each game tick"""
        self.update_events()
        self.update_camera()

    def update_camera(self):
        """if move keys are pressed, move the camera and cache the visible tiles"""
        movex = self.movex
        movey = self.movey
        self.cam_pos_old = self.cam_rect.topleft
        if movex or movey:
            self.cam_rect.x += movex * self.scroll_speed
            self.cam_rect.y += movey * self.scroll_speed
            self.cam_rect.clamp_ip(self.world_rect)
            self.cache_visible_tiles()

    def cache_visible_tiles(self):
        del self.visible_tiles[:]
        # calculate the visible bounds as array indices
        old_x, old_y = self.cam_pos_old
        cam_rect = self.cam_rect
        cam_rect.clamp_ip(self.world_rect)
        mw, mh = self.map_size
        tw, th = self.tile_size
        x = min(cam_rect.x, old_x) // tw
        y = min(cam_rect.y, old_y) // th
        # pad w and h to fetch-ahead for interpolation
        w = cam_rect.w // tw + max(self.scroll_speed // tw, 1) * 3
        h = cam_rect.h // th + max(self.scroll_speed // th, 1) * 3
        # Don't allow x or y to be negative, it will mess up the slice
        if x < 0:
            w -= x
            x = 0
        if y < 0:
            h -= y
            y = 0
        # slice each row in the visible range
        for row in range(y, y + h):
            start = row * mw + x
            end = start + w
            self.visible_tiles.extend(self.tiles[start:end])

    def update_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                self.on_quit(e)
            elif e.type == KEYDOWN:
                self.on_keydown(e)
            elif e.type == KEYUP:
                self.on_keyup(e)

    def update_caption(self, dt):
        cam = tuple(self.cam_rect)
        cap = 'FPS {} | Visible {} | Camera {}'.format(int(self.clock.get_fps()), len(self.visible_tiles), cam)
        pygame.display.set_caption(cap)

    def on_quit(self, e):
        self.running = False

    def on_keydown(self, e):
        key = e.key
        if key == K_ESCAPE:
            self.running = False
        elif key == K_DOWN:
            self.movey += 1
        elif key == K_RIGHT:
            self.movex += 1
        elif key == K_UP:
            self.movey -= 1
        elif key == K_LEFT:
            self.movex -= 1

    def on_keyup(self, e):
        key = e.key
        if key == K_DOWN:
            self.movey -= 1
        elif key == K_RIGHT:
            self.movex -= 1
        elif key == K_UP:
            self.movey += 1
        elif key == K_LEFT:
            self.movex += 1

    def draw(self, interp):
        """draw the visible sprites which are cached"""
        screen = self.screen
        screen.fill(self.bgcolor)
        blit = screen.blit
        # calculate interpolation to add steps to the scrolling; this smooths the appearance
        cam_rect = self.cam_rect
        cx, cy = cam_rect.x, cam_rect.y
        ox, oy = self.cam_pos_old
        xd = int((cx - ox) * (1.0 - interp))
        yd = int((cy - oy) * (1.0 - interp))
        # render the sprites, translating their world coordinates to the screen
        for sprite in self.visible_tiles:
            rect = sprite.rect
            # rect.x = sprite.rect.x - cx + xd
            # rect.y = sprite.rect.y - cy + yd
            blit(sprite.image, rect.move(-cx + xd, -cy + yd))
        pygame.display.flip()


if __name__ == '__main__':
    parse_args()
    pygame.init()
    game = Game(CONFIG['screen'], CONFIG['tilesize'], CONFIG['mapsize'])
    game.run()
