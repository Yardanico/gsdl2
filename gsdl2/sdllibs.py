"""dynamiclibs.py
"""
import sdl

__all__ = [
    'sdl_lib', 'image_lib', 'ttf_lib', 'mixer_lib', 'gfx_lib',
    'SDL_LIBS', 'SDLIMAGE_LIBS', 'SDLTTF_LIBS', 'SDLMIXER_LIBS', 'SDLGFX_LIBS',
    'SDLError',
]


from gsdl2.sdlffi import *


class SDLError(Exception):

    def __init__(self):
        message = sdl.ffi.string(sdl.getError()).decode('utf-8')
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


SDLGFX_LIBS = ['SDL2_gfx.dll', 'libSDL2_gfx.so', 'libSDL2_gfx-1.0.so.0']
gfx_lib = dlopen(gfx_ffi, SDLGFX_LIBS)
