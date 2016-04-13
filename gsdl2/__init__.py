import logging


__all__ = [
    'init', 'Clock', 'Color', 'GameClock', 'Font', 'Rect', 'Renderer', 'Surface', 'SysFont', 'Texture', 'Window',
    'sdlconstants', 'sdlkeys', 'sdl_ffi', 'image_ffi', 'ttf_ffi', 'sdl_lib', 'image_lib', 'ttf_lib', 'color',
    'colordict', 'display', 'draw', 'event', 'font', 'gameclock', 'image', 'joystick', 'mixer', 'mouse', 'music',
    'particles', 'rect', 'renderer', 'surface', 'time', 'texture', 'window', 'utf8'
]


#==============================================================================
#      _____ _____  _      ___
#     / ____|  __ \| |    |__ \
#    | (___ | |  | | |       ) |
#     \___ \| |  | | |      / /
#     ____) | |__| | |____ / /_
#    |_____/|_____/|______|____|
#
#==============================================================================


#-----------------------------------
# FFI, Dynamic libs, Constants, Keys
#-----------------------------------

from . import sdlffi
from . import sdllibs
from . import sdlconstants

sdl_ffi = sdlffi.sdl_ffi
sdl_lib = sdllibs.sdl_lib

image_ffi = sdlffi.image_ffi
image_lib = sdllibs.image_lib

ttf_ffi = sdlffi.ttf_ffi
ttf_lib = sdllibs.ttf_lib

mixer_ffi = sdlffi.mixer_ffi
mixer_lib = sdllibs.mixer_lib



#==============================================================================
#      _____  _____ _____  _      ___
#     / ____|/ ____|  __ \| |    |__ \
#    | |  __| (___ | |  | | |       ) |
#    | | |_ |\___ \| |  | | |      / /
#    | |__| |____) | |__| | |____ / /_
#     \_____|_____/|_____/|______|____|
#
#==============================================================================


#-----------------------------------
# Modules
#-----------------------------------

from . import color
from . import colordict
from . import event
from . import image
from . import joystick
from . import mixer
from . import mouse
from . import music
from . import rect
from . import renderer
from . import surface
from . import font
from . import _time as time
from . import texture
from . import window
from . import display
from . import draw
from . import particles
from . import locals


#-----------------------------------
# Classes and constants
#-----------------------------------

from .color import Color
from ._time import Clock, GameClock
from .font import Font, SysFont
from .rect import Rect
from .renderer import Renderer
from .surface import Surface
from .texture import Texture
from .window import Window
from .locals import *


#-----------------------------------
# Startup and Shutdown
#-----------------------------------

import atexit


def init():
    rc = sdl_lib.SDL_Init(sdlconstants.SDL_INIT_EVERYTHING)
    if rc != 0:
        logging.log(logging.ERROR, 'SDL2 failed to initialize')
        raise Exception('SDL2: failed to initialize')

    rc = sdl_lib.SDL_SetHint(utf8(sdlconstants.SDL_HINT_RENDER_SCALE_QUALITY), utf8("1"))
    if rc == 0:
        logging.log(logging.ERROR, 'SDL2: failed to set hint {}'.format(sdlconstants.SDL_HINT_RENDER_SCALE_QUALITY))
        logging.log(logging.ERROR, sdl_lib.SDL_GetError())

    rc = image_lib.IMG_Init(sdlconstants.IMG_INIT_EVERYTHING)
    if rc == 0:
        logging.log(logging.ERROR, 'SDL2_image: failed to initialize')
        logging.log(logging.ERROR, sdl_lib.SDL_GetError())
    elif not rc & sdlconstants.MIX_INIT_EVERYTHING:
        logging.log(logging.WARN, 'SDL2_image: some libraries failed to load: rc={}'.format(rc))

    rc = ttf_lib.TTF_Init()
    if rc != 0:
        logging.log(logging.ERROR, 'SDL2_ttf: failed to initialize')
        logging.log(logging.ERROR, sdl_lib.SDL_GetError())

    rc = mixer_lib.Mix_Init(sdlconstants.MIX_INIT_EVERYTHING)
    if rc == 0:
        logging.log(logging.ERROR, 'SDL2_mixer: failed to initialize')
        logging.log(logging.ERROR, sdl_lib.SDL_GetError())
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
    sdl_lib.SDL_Quit()
    image_lib.IMG_Quit()
    ttf_lib.TTF_Quit()
    mixer_lib.Mix_CloseAudio()
    mixer_lib.Mix_Quit()


def _atexit():
    # Experimental: trying to encourage pypy to collect garbage
    del window.get_list()[:]
    display.Runtime.window = None
    display.Runtime.renderer = None
