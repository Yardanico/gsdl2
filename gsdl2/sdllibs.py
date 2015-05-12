"""dynamiclibs.py
"""


__all__ = [
    'sdl_lib', 'image_lib', 'ttf_lib', 'mixer_lib',
    'SDL_LIBS', 'SDLIMAGE_LIBS', 'SDLTTF_LIBS', 'SDLMIXER_LIBS',
    'SDLError',
]


import logging

from .sdlffi import *


class SDLError(Exception):

    def __init__(self):
        message = sdl_ffi.string(sdl_lib.SDL_GetError()).decode('utf-8')
        Exception.__init__(self, message)


def dlopen(ffi, names):
    for name in names:
        try:
            lib = ffi.dlopen(name)
            # print('Found {}'.format(name))
            return lib
        except OSError:
            pass
    return ffi.dlopen(names[0])


SDL_LIBS = ['SDL2.dll', 'libSDL2.so', 'libSDL2-2.0.so.0']
sdl_lib = dlopen(sdl_ffi, SDL_LIBS)

SDLTTF_LIBS = ['SDL2_ttf.dll', 'libSDL2_ttf.so', 'libSDL2_ttf-2.0.so.0']
ttf_lib = dlopen(ttf_ffi, SDLTTF_LIBS)

SDLIMAGE_LIBS = ['SDL2_image.dll', 'libSDL2_image.so', 'libSDL2_image-2.0.so.0']
image_lib = dlopen(image_ffi, SDLIMAGE_LIBS)

SDLMIXER_LIBS = ['SDL2_mixer.dll', 'libSDL2_mixer.so', 'libSDL2_mixer-2.0.so.0']
mixer_lib = dlopen(mixer_ffi, SDLMIXER_LIBS)
