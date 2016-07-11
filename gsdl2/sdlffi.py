__all__ = ['sdl_ffi', 'image_ffi', 'ttf_ffi', 'mixer_ffi']


from . import sdl
from . import sdlttf
from . import sdlimage
from . import sdlmixer


sdl_ffi = sdl.ffi
ttf_ffi = sdlttf.ffi
image_ffi = sdlimage.ffi
mixer_ffi = sdlmixer.ffi


def to_string(cdata, encoding='utf-8'):
    return sdl_ffi.string(cdata).decode(encoding)
