import logging

import _sdl

__all__ = [
    'init', 'Clock', 'Color', 'GameClock', 'Font', 'Rect', 'Renderer', 'Surface', 'SysFont', 'Texture', 'Window',
    'sdlconstants',
    'color', 'colordict', 'display', 'draw', 'event', 'font', 'gameclock', 'gfx', 'image', 'joystick', 'mixer', 'mouse',
    'music', 'particles', 'rect', 'renderer', 'surface', 'time', 'texture', 'window', 'utf8', 'transform', 'ffi'
]

# ==============================================================================
#      _____ _____  _      ___
#     / ____|  __ \| |    |__ \
#    | (___ | |  | | |       ) |
#     \___ \| |  | | |      / /
#     ____) | |__| | |____ / /_
#    |_____/|_____/|______|____|
#
# ==============================================================================


# -----------------------------------
# FFI, Dynamic libs, Constants, Keys
# -----------------------------------

import sdl
from gsdl2 import sdlffi
from gsdl2 import sdllibs
from gsdl2 import sdlconstants

gfx_lib = sdllibs.gfx_lib
ffi = sdl.ffi
SDLError = sdl.SDLError

# ==============================================================================
#      _____  _____ _____  _      ___
#     / ____|/ ____|  __ \| |    |__ \
#    | |  __| (___ | |  | | |       ) |
#    | | |_ |\___ \| |  | | |      / /
#    | |__| |____) | |__| | |____ / /_
#     \_____|_____/|_____/|______|____|
#
# ==============================================================================


# -----------------------------------
# Modules
# -----------------------------------
from gsdl2 import cursors
from gsdl2 import color
from gsdl2 import colordict
from gsdl2 import event
from gsdl2 import image
from gsdl2 import joystick
from gsdl2 import mixer
from gsdl2 import mouse
from gsdl2 import music
from gsdl2 import rect
from gsdl2 import renderer
from gsdl2 import surface
from gsdl2 import font
from gsdl2 import _time as time
from gsdl2 import texture
from gsdl2 import window
from gsdl2 import display
from gsdl2 import draw
from gsdl2 import gfx
from gsdl2 import particles
from gsdl2 import locals
from gsdl2 import key
from gsdl2 import time
from gsdl2 import transform
# -----------------------------------
# Classes and constants
# -----------------------------------

from gsdl2.color import Color
from gsdl2._time import Clock, GameClock
from gsdl2.font import Font, SysFont
from gsdl2.rect import Rect
from gsdl2.renderer import Renderer
from gsdl2.surface import Surface
from gsdl2.texture import Texture
from gsdl2.window import Window
from gsdl2.locals import *
from gsdl2.sprite import *
# -----------------------------------
# Startup and Shutdown
# -----------------------------------

import atexit

# TODO: not sure whether it should be True or False
HAVE_NEWBUF = False

_quit_functions = []


def register_quit(quit_func):
    _quit_functions.append(quit_func)


def get_sdl_byteorder():
    return sdlconstants.SDL_BYTEORDER


def get_sdl_version():
    ver = sdl.getVersion(())
    return ver.major, ver.minor, ver.patch


def get_error():
    sdl.getError()


def sdl_sleep(mills):
    sdl.delay(mills)


def init():
    rc = sdl.init(sdlconstants.SDL_INIT_EVERYTHING)
    if rc != 0:
        logging.log(logging.ERROR, 'SDL2 failed to initialize')
        raise Exception('SDL2: failed to initialize')

    rc = sdl.setHint(utf8(sdlconstants.SDL_HINT_RENDER_SCALE_QUALITY), utf8("1"))
    if rc == 0:
        logging.log(logging.ERROR, 'SDL2: failed to set hint {}'.format(sdlconstants.SDL_HINT_RENDER_SCALE_QUALITY))
        logging.log(logging.ERROR, sdl.getError())

    rc = sdl.image.init(sdlconstants.IMG_INIT_EVERYTHING)
    if rc == 0:
        logging.log(logging.ERROR, 'SDL2_image: failed to initialize')
        logging.log(logging.ERROR, sdl.getError())
    elif not rc & sdlconstants.MIX_INIT_EVERYTHING:
        logging.log(logging.WARN, 'SDL2_image: some libraries failed to load: rc={}'.format(rc))

    rc = sdl.ttf.init()
    if rc != 0:
        logging.log(logging.ERROR, 'SDL2_ttf: failed to initialize')
        logging.log(logging.ERROR, sdl.getError())

    rc = sdl.mixer.init(sdlconstants.MIX_INIT_EVERYTHING)
    if rc == 0:
        logging.log(logging.ERROR, 'SDL2_mixer: failed to initialize')
        logging.log(logging.ERROR, sdl.getError())
    elif not rc & sdlconstants.MIX_INIT_EVERYTHING:
        logging.log(logging.WARN, 'SDL2_mixer: some libraries failed to load: rc={}'.format(rc))
        lib2name = dict(
            MIX_INIT_FLAC='MIX_INIT_FLAC',
            MIX_INIT_MOD='MIX_INIT_MOD',
            MIX_INIT_MODPLUG='MIX_INIT_MODPLUG',
            MIX_INIT_MP3='MIX_INIT_MP3',
            MIX_INIT_OGG='MIX_INIT_OGG',
            MIX_INIT_FLUIDSYNTH='MIX_INIT_FLUIDSYNTH',
        )
        for lib in (
                sdlconstants.MIX_INIT_FLAC,
                sdlconstants.MIX_INIT_MOD,
                sdlconstants.MIX_INIT_MODPLUG,
                sdlconstants.MIX_INIT_MP3,
                sdlconstants.MIX_INIT_OGG,
                sdlconstants.MIX_INIT_FLUIDSYNTH):
            if rc & lib:
                logging.log(logging.WARN, 'SDL2_mixer: {} failed'.format(lib2name[lib]))

    atexit.register(_atexit)


def quit():
    for quit_func in reversed(_quit_functions):
        quit_func()
    # exit sdl2
    sdl.quit()
    # exit sdl2 image
    sdl.image.quit()
    # exit sdl2 ttf
    sdl.ttf.quit()
    # close audio and exit sdl2 mixer
    sdl.mixer.closeAudio()
    sdl.mixer.quit()


def _atexit():
    # Experimental: trying to encourage pypy to collect garbage
    del window.get_list()[:]
    display.Runtime.window = None
    display.Runtime.renderer = None
