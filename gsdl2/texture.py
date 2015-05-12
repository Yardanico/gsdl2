__all__ = ['Texture']


import logging

from .sdllibs import sdl_lib
from .rect import Rect


log = logging.getLogger(__name__)


class Texture(object):

    # def __init__(self, renderer=None, surface=None):
    #     if surface:
    #         assert renderer is not None
    #         self.__sdl_texture = sdl_lib.SDL_CreateTextureFromSurface(renderer.sdl_renderer, surface.sdl_surface)
    #         self.__size = surface.get_size()

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
