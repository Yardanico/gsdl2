__all__ = ['Texture']


import logging

import cffi

from .sdllibs import sdl_lib
from .sdlffi import sdl_ffi
from .rect import Rect


log = logging.getLogger(__name__)


class Texture(object):
    def __init__(self, renderer, surface):
        self.__sdl_texture = sdl_lib.SDL_CreateTextureFromSurface(renderer.sdl_renderer, surface.sdl_surface)
        self.__size = surface.get_size()

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
        return cdata[0]

    def set_blendmode(self, mode):
        sdl_lib.SDL_SetTextureBlendMode(self.sdl_texture, mode)

    def get_alpha(self):
        cdata = sdl_ffi.new('Uint8 *')
        sdl_lib.SDL_GetTextureAlphaMod(self.sdl_texture, cdata)
        return cdata[0]

    def set_alpha(self, alpha):
        sdl_lib.SDL_SetTextureAlphaMod(self.sdl_texture, int(alpha))

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
