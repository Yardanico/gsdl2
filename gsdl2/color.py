__all__ = ['Color']


import logging

from .sdlffi import sdl_ffi
from .colordict import THECOLORS


log = logging.getLogger(__name__)


class Color(object):

    # This is used to iterate slices in __getitem__.
    __i2a = {0: 'r', 1: 'g', 2: 'b', 3: 'a'}

    def __init__(self, *args):
        assert len(args)

        self.__color = [0] * 4
        self.__sdl_color = sdl_ffi.new('SDL_Color *')

        if isinstance(args[0], str):
            color_name = args[0]
            if color_name in THECOLORS:
                c = THECOLORS[color_name]
                self.r = c[0]
                self.g = c[1]
                self.b = c[2]
                self.a = c[3]
            else:
                raise Exception('invalid color name {}'.format(color_name))
        else:
            self.r = args[0]
            self.g = args[1]
            self.b = args[2]
            self.a = 255 if len(args) == 3 else args[3]

    def __getr(self):
        return self.__color[0]
    def __setr(self, r):
        self.__color[0] = r
        self.__sdl_color.r = r
    r = property(__getr, __setr)

    def __getg(self):
        return self.__color[1]
    def __setg(self, g):
        self.__color[1] = g
        self.__sdl_color.g = g
    g = property(__getg, __setg)

    def __getb(self):
        return self.__color[2]
    def __setb(self, b):
        self.__color[2] = b
        self.__sdl_color.b = b
    b = property(__getb, __setb)

    def __geta(self):
        return self.__color[3]
    def __seta(self, a):
        self.__color[3] = a
        self.__sdl_color.a = a
    a = property(__geta, __seta)

    def __get_sdl_color(self):
        return self.__sdl_color
    sdl_color = property(__get_sdl_color)

    def __iter__(self):
        for c in self.__color:
            yield c

    def __getitem__(self, i):
        return self.__color[i]

    def __setitem__(self, key, value):
        c = self.__color
        c[key] = value
        self.r = c[0]
        self.g = c[1]
        self.b = c[2]
        self.a = c[3]

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __len__(self):
        return 4

    def __str__(self):
        return '<{}({}, {}, {}, {})>'.format(self.__class__.__name__, *self[:])
