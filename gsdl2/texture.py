__all__ = ['Texture']


import logging

import cffi

from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
from .rect import Rect
from . import sdlpixels


log = logging.getLogger(__name__)


class Texture(object):
    def __init__(self, renderer, surface=None, size=None, sdl_texture=None):
        if surface:
            # print('texture from surface')
            self.__sdl_texture = sdl_lib.SDL_CreateTextureFromSurface(renderer.sdl_renderer, surface.sdl_surface)
            self.__size = surface.get_size()
        elif sdl_texture:
            # print('texture from sdl texture')
            self.__sdl_texture = sdl_texture
            # print(self.query())
            format, access, w, h = self.query()
            self.__size = w, h
        else:
            # print('texture from scratch')
            # print('SDL_TEXTUREACCESS_TARGET', sdl_lib.SDL_TEXTUREACCESS_TARGET)
            self.__sdl_texture = sdl_lib.SDL_CreateTexture(
                renderer.sdl_renderer,
                sdlpixels.SDL_PIXELFORMAT_ARGB8888,
                sdl_lib.SDL_TEXTUREACCESS_TARGET, *size)
            # print(self.query())
            self.__size = tuple(size)

    def query(self):
        format = sdl_ffi.new('Uint32 *')
        access = sdl_ffi.new('int *')
        w = sdl_ffi.new('int *')
        h = sdl_ffi.new('int *')
        sdl_lib.SDL_QueryTexture(self.sdl_texture, format, access, w, h)
        # return int(format[0]), int(access[0]), int(w[0]), int(h[0])
        return format[0], access[0], w[0], h[0]

    def get_size(self):
        return self.__size
    size = property(get_size)

    def get_rect(self, **kwargs):
        w, h = self.__size
        r = Rect(0, 0, w, h)
        for k, v in kwargs.items():
            setattr(r, k, v)
        return r

    def get_blendmode(self):
        cdata = sdl_ffi.new('SDL_BlendMode *')
        sdl_lib.SDL_GetTextureBlendMode(self.sdl_texture, cdata)
        value = int(cdata[0])
        return value
    def set_blendmode(self, mode):
        sdl_lib.SDL_SetTextureBlendMode(self.sdl_texture, mode)
    blendmode = property(get_blendmode, set_blendmode)

    def get_alpha(self):
        cdata = sdl_ffi.new('Uint8 *')
        sdl_lib.SDL_GetTextureAlphaMod(self.sdl_texture, cdata)
        return cdata[0]
    def set_alpha(self, alpha):
        sdl_lib.SDL_SetTextureAlphaMod(self.sdl_texture, int(alpha))
    alpha = property(get_alpha, set_alpha)

    def __getsdltexture(self):
        return self.__sdl_texture
    sdl_texture = property(__getsdltexture)

    def __del__(self):
        # TODO: unreliable
        if self.__sdl_texture:
            try:
                garbage = self.__sdl_texture
                self.__sdl_texture = None
                sdl_lib.SDL_DestroyTexture(garbage)
            except Exception as e:
                pass
