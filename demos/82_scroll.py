"""82_scroll.py - many, many scrolling tiles using the texture renderer

Usage: python 82_scroll.py [tilesize=WxH] [mapsize=WxH] [screen=WxH]

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
    python 82_scroll.py tilesize=64x64
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
from gsdl2.locals import Rect, Color, QUIT, KEYDOWN, KEYUP, S_ESCAPE, S_SPACE, S_LEFT, S_RIGHT, S_UP, S_DOWN


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

    # textures
    tile_images = []

    def __init__(self, resolution, tile_size, map_size):
        self.tile_size = tile_size
        self.map_size = map_size
        self.screen = gsdl2.display.set_mode(resolution)
        self.screen_rect = self.screen.get_rect()

        self.bgcolor = Color('black')

        # define the world as a rect; these are absolute coords
        mw, mh = map_size
        tw, th = tile_size
        self.world_rect = Rect(0, 0, tw * mw, th * mh)

        # load textures
        if not Game.tile_images:
            renderer = gsdl2.display.get_renderer()
            for color_name in 'green1', 'green2', 'green3', 'green4':
                color = Color(color_name)
                tile_image = gsdl2.Surface((tw, th))
                tile_image.fill(color)
                gsdl2.draw.rect(tile_image, Color('white'), Rect(0, 0, tw, th), 1)
                tx = gsdl2.texture.Texture(renderer, tile_image)
                Game.tile_images.append(tx)

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

        # make the clock and schedule a few callbacks
        self.clock = gsdl2.time.GameClock(update_callback=self.update, frame_callback=self.draw)
        self.clock.schedule_interval(self.update_caption, 0.1)
        self.running = False

    def run(self):
        """drive the clock; the clock will call update(), draw(), and update_caption() on schedule"""
        self.running = True
        while self.running:
            self.clock.tick()

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
        for e in gsdl2.event.get():
            if e.type == QUIT:
                self.on_quit(e)
            elif e.type == KEYDOWN:
                self.on_keydown(e)
            elif e.type == KEYUP:
                self.on_keyup(e)

    def update_caption(self, dt):
        cam = tuple(self.cam_rect)
        cap = 'FPS {} | Visible {} | Camera {}'.format(self.clock.fps, len(self.visible_tiles), cam)
        gsdl2.display.set_caption(cap)

    def on_quit(self, e):
        self.running = False

    def on_keydown(self, e):
        code = e.scancode
        if code == S_ESCAPE:
            self.running = False
        elif code == S_DOWN:
            self.movey += 1
        elif code == S_RIGHT:
            self.movex += 1
        elif code == S_UP:
            self.movey -= 1
        elif code == S_LEFT:
            self.movex -= 1

    def on_keyup(self, e):
        code = e.scancode
        if code == S_DOWN:
            self.movey -= 1
        elif code == S_RIGHT:
            self.movex -= 1
        elif code == S_UP:
            self.movey += 1
        elif code == S_LEFT:
            self.movex += 1

    def draw(self, interp):
        """draw the visible sprites which are cached"""
        renderer = gsdl2.display.get_renderer()
        renderer.clear()
        # calculate interpolation to add steps to the scrolling; this smooths the appearance
        cam_rect = self.cam_rect
        cx, cy = cam_rect.x, cam_rect.y
        ox, oy = self.cam_pos_old
        xd = -cx + int((cx - ox) * (1.0 - interp))
        yd = -cy + int((cy - oy) * (1.0 - interp))
        # render the sprites, translating their world coordinates to the screen
        rect = self.scrap_rect
        for sprite in self.visible_tiles:
            rect.x = sprite.rect.x + xd
            rect.y = sprite.rect.y + yd
            renderer.copy(sprite.image, rect)
        renderer.present()


if __name__ == '__main__':
    parse_args()
    gsdl2.init()
    game = Game(CONFIG['screen'], CONFIG['tilesize'], CONFIG['mapsize'])
    game.run()
