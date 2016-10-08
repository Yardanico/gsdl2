import sdl

import gsdl2

__all__ = ['Color']

import logging

from gsdl2.colordict import THECOLORS

COLORS = THECOLORS  # better-looking :)
log = logging.getLogger(__name__)

# http://stackoverflow.com/questions/4296249/how-do-i-convert-a-hex-triplet-to-an-rgb-tuple-and-back
_NUMERALS = '0123456789abcdefABCDEF'
_HEXDEC = {v: int(v, 16) for v in (x + y for x in _NUMERALS for y in _NUMERALS)}


def rgb(triplet):
    return _HEXDEC[triplet[0:2]], _HEXDEC[triplet[2:4]], _HEXDEC[triplet[4:6]]


class Color(object):
    # This is used to iterate slices in __getitem__.
    __i2a = {0: 'r', 1: 'g', 2: 'b', 3: 'a'}

    def __init__(self, *args):
        assert len(args)

        self.__color = [0] * 4
        self.__sdl_color = sdl.Color()  # sdl.ffi.new('SDL_Color *')
        if isinstance(args[0], (str, unicode)):
            color_name = args[0]
            if color_name in THECOLORS:  # if we have color in COLORDICT
                c = THECOLORS[color_name]
                self.r = c[0]
                self.g = c[1]
                self.b = c[2]
                self.a = c[3]
            elif '#' in color_name:  # if color is in hex format
                r, g, b = rgb(color_name.replace("#", ''))
                self.r = r
                self.g = g
                self.b = b
                self.a = 255
            else:
                raise Exception('Invalid color argument {}'.format(color_name))

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
        return self.__sdl_color.cdata[0]

    sdl_color = property(__get_sdl_color)

    def __repr__(self):
        return "<gsdl2.Color r=%i, g=%i, b=%i>" % (self.r, self.g, self.b)

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


# convert color or many colors from tuple or r, g, b ints
def convert_to_color(*color_values):
    color_result = []
    for color_value in color_values:
        if not color_value:
            color_result.append(None)
        elif not isinstance(color_value, gsdl2.Color):
            # if it's tuple, let's create a color
            if isinstance(color_value, tuple):
                color = gsdl2.Color(*color_value)
            else:
                color = gsdl2.Color(color_value)
            color_result.append(color)
        else:
            color_result.append(color_value)
    return color_result[0] if len(color_result) == 1 else color_result


def _check_range(val):
    if not 0 <= val <= 255:
        raise ValueError("Color should be between 0 and 255")
    return val


def create_color(color, color_format):
    if isinstance(color, (int, long)):
        return color
    if isinstance(color, Color):
        return sdl.mapRGBA(color_format, color.r, color.g, color.b,
                           color.a)
    if isinstance(color, tuple) and len(color) == 1:
        return create_color(color[0], color_format)
    if hasattr(color, '__iter__') and 3 <= len(color) <= 4:
        if len(color) == 3:
            a = 255
        else:
            a = _check_range(color[3])
        return sdl.mapRGBA(color_format, _check_range(color[0]),
                           _check_range(color[1]),
                           _check_range(color[2]), a)
    raise ValueError("Unrecognized color format %s" % (color,))
