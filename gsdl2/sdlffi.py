__all__ = ['ffi', 'gfx_ffi']

from sdl import ffi
from . import sdlgfx

gfx_ffi = sdlgfx.ffi


def to_string(cdata, encoding='utf-8'):
    return ffi.string(cdata).decode(encoding)
